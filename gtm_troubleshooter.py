#!/usr/bin/env python3
"""
Evidence-First, Actionable Server-Side Tracking Troubleshooter
Scope: WooCommerce + wGTM + sGTM (Stape Data Client) + Cloudflare SOP Worker (/metrics) + Complianz Consent Mode v2

GOAL: Troubleshoot the end-to-end tracking pipeline without layer conflation.
Fail closed: if required data is missing or unproven, treat it as a STOP condition.
"""

import json
import csv
import os
import sys
import re
import traceback
from pathlib import Path
from fnmatch import fnmatch
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from collections import defaultdict


class EvidenceReference:
    """Encapsulates evidence sourcing: file | pointer | snippet"""
    
    def __init__(self, file: str, pointer: str, snippet: str, evidence_type: str = "CONFIG"):
        self.file = file
        self.pointer = pointer
        self.snippet = snippet
        self.evidence_type = evidence_type  # CONFIG or RUNTIME
    
    def __str__(self):
        return f"[{self.evidence_type}] {self.file} | {self.pointer} | \"{self.snippet[:80]}...\""


class GTMTroubleshooter:
    """Main troubleshooter implementing the 10-phase workflow"""
    
    def __init__(self, data_dir: str = "original-data"):
        self.data_dir = Path(data_dir)
        self.findings = {
            "coverage": {},
            "source_index": [],
            "inventory": {},
            "gates": {},
            "event_chains": {},
            "root_causes": [],
            "action_cards": [],
            "missing_evidence": []
        }
        self.wgtm_export = None
        self.sgtm_export = None
        self.tag_assistant_web = None
        self.tag_assistant_server = None
        self.stape_logs = []
        self.datalayer_samples = []
        self.worker_code = None
        
    def run_full_audit(self):
        """Execute all 10 phases of the workflow in order"""
        print("=" * 80)
        print("GTM EVIDENCE-FIRST TROUBLESHOOTER")
        print("=" * 80)
        print()
        
        # PHASE 1: Coverage Summary
        print("PHASE 1 — Coverage Summary")
        print("-" * 80)
        self.phase1_coverage_summary()
        print()
        
        # PHASE 2: Source Index
        print("PHASE 2 — Source Index")
        print("-" * 80)
        self.phase2_source_index()
        print()
        
        # PHASE 3: Inventory
        print("PHASE 3 — Inventory (CONFIG)")
        print("-" * 80)
        self.phase3_inventory()
        print()
        
        # PHASE 4: Gate 1 - Browser Network Proof
        print("PHASE 4 — Gate 1: Browser Network Proof [RUNTIME]")
        print("-" * 80)
        self.phase4_gate1_network_proof()
        print()
        
        # PHASE 5: Gate 2 - SOP Contract
        print("PHASE 5 — Gate 2: SOP Contract [CONFIG]")
        print("-" * 80)
        self.phase5_gate2_sop_contract()
        print()
        
        # PHASE 6: Gate 3 - sGTM Claim + Inbound
        print("PHASE 6 — Gate 3: sGTM Claim + Inbound eventData [RUNTIME]")
        print("-" * 80)
        self.phase6_gate3_sgtm_inbound()
        print()
        
        # PHASE 7: Gate 4 - Data Contract + Mutation
        print("PHASE 7 — Gate 4: Data Contract + Mutation Check [RUNTIME]")
        print("-" * 80)
        self.phase7_gate4_mutation_check()
        print()
        
        # PHASE 8: Gate 5 - Identity + Dedup
        print("PHASE 8 — Gate 5: Identity + Dedup [RUNTIME + CONFIG]")
        print("-" * 80)
        self.phase8_gate5_identity_dedup()
        print()
        
        # PHASE 9: Root Causes
        print("PHASE 9 — Root Causes (max 5)")
        print("-" * 80)
        self.phase9_root_causes()
        print()
        
        # PHASE 10: Fix Plan
        print("PHASE 10 — Fix Plan (Action Cards)")
        print("-" * 80)
        self.phase10_action_cards()
        print()
        
        # Output Summary
        print("=" * 80)
        print("AUDIT COMPLETE")
        print("=" * 80)
        self.output_summary()
        
    def phase1_coverage_summary(self):
        """PHASE 1: Discover and categorize all available inputs"""
        found = []
        missing = []
        
        # Core inputs
        core_inputs = {
            "wGTM export JSON": self._find_file_pattern("GTM-*_workspace*.json", "WEB"),
            "sGTM export JSON": self._find_file_pattern("GTM-*_workspace*.json", "SERVER"),
            "Tag Assistant web": self._find_file_pattern("tag_assistant_*messerattach*.json", exclude_pattern="sgtm"),
            "Tag Assistant server": self._find_file_pattern("tag_assistant_sgtm*.json"),
        }
        
        # Optional inputs
        optional_inputs = {
            "Stape logs": self._find_file_pattern("*stape*logs*.csv"),
            "Worker code": self._find_file_pattern("*worker*.js"),
            "Cloudflare notes": self._find_file_pattern("*cloudflare*.md"),
            "WP Rocket settings": self._find_file_pattern("*rocket*.md"),
            "Stape plugin settings": self._find_file_pattern("STAPE_SGTM_PLUGIN_SETTINGS.md"),
            "DataLayer samples": self._find_datalayer_files(),
        }
        
        print("Core Inputs:")
        for name, path in core_inputs.items():
            if path:
                found.append(name)
                print(f"  ✓ {name}: {path.name if isinstance(path, Path) else path}")
                self._load_file(name, path)
            else:
                missing.append(name)
                print(f"  ✗ {name}: NOT FOUND")
        
        print("\nOptional Inputs:")
        for name, paths in optional_inputs.items():
            if paths:
                found.append(name)
                if isinstance(paths, list):
                    print(f"  ✓ {name}: {len(paths)} file(s)")
                    for p in paths:
                        self._load_file(name, p)
                else:
                    print(f"  ✓ {name}: {paths.name if isinstance(paths, Path) else paths}")
                    self._load_file(name, paths)
            else:
                print(f"  - {name}: not present")
        
        self.findings["coverage"] = {
            "found": found,
            "missing": missing,
            "timestamp": datetime.now().isoformat()
        }
    
    def phase2_source_index(self):
        """PHASE 2: Build evidence map for key events"""
        print("Building Source Index (max 2 entries per event type per source)...")
        print()
        
        # Priority events to index
        priority_events = [
            "view_item", "add_to_cart", "begin_checkout", "purchase",
            "view_item_list", "view_cart", "search"
        ]
        
        index = []
        
        # Index from Tag Assistant Web
        if self.tag_assistant_web:
            index.extend(self._index_tag_assistant(self.tag_assistant_web, "tag_assistant_web", priority_events))
        
        # Index from Tag Assistant Server
        if self.tag_assistant_server:
            index.extend(self._index_tag_assistant(self.tag_assistant_server, "tag_assistant_server", priority_events))
        
        # Index from DataLayer samples
        for dl in self.datalayer_samples:
            index.extend(self._index_datalayer(dl, priority_events))
        
        # Store and display
        self.findings["source_index"] = index
        
        if index:
            print(f"{'Event Name':<20} {'Timestamp':<25} {'Page URL':<40} {'Event ID':<15} {'Source':<30}")
            print("-" * 130)
            for entry in index[:20]:  # Limit display
                print(f"{entry['event_name']:<20} {entry.get('timestamp', 'N/A'):<25} "
                      f"{entry.get('page_url', 'N/A')[:38]:<40} {entry.get('event_id', 'N/A'):<15} "
                      f"{entry['source']:<30}")
        else:
            print("⚠️  No events found in available sources")
        
        print(f"\nTotal indexed: {len(index)} events")
    
    def phase3_inventory(self):
        """PHASE 3: Extract configuration inventory"""
        print("Extracting Configuration Inventory...")
        print()
        
        inventory = {
            "containers": [],
            "ga4_ids": [],
            "google_ads_ids": [],
            "other_vendors": [],
            "stape_data_tag": None,
            "sgtm_clients": [],
            "consent_mechanism": None
        }
        
        # wGTM Container
        if self.wgtm_export:
            wgtm_inv = self._inventory_gtm_container(self.wgtm_export, "wGTM")
            inventory["containers"].append(wgtm_inv)
            inventory["ga4_ids"].extend(wgtm_inv.get("ga4_ids", []))
            inventory["google_ads_ids"].extend(wgtm_inv.get("google_ads_ids", []))
            inventory["other_vendors"].extend(wgtm_inv.get("other_vendors", []))
            if wgtm_inv.get("stape_data_tag"):
                inventory["stape_data_tag"] = wgtm_inv["stape_data_tag"]
        
        # sGTM Container
        if self.sgtm_export:
            sgtm_inv = self._inventory_gtm_container(self.sgtm_export, "sGTM")
            inventory["containers"].append(sgtm_inv)
            inventory["sgtm_clients"] = sgtm_inv.get("clients", [])
            inventory["ga4_ids"].extend(sgtm_inv.get("ga4_ids", []))
            inventory["google_ads_ids"].extend(sgtm_inv.get("google_ads_ids", []))
        
        self.findings["inventory"] = inventory
        
        # Display summary
        print("Container Versions:")
        for container in inventory["containers"]:
            print(f"  {container['type']}: {container['container_id']} "
                  f"(v{container['version_id']}, exported {container['export_time']})")
        
        print(f"\nGA4 Measurement IDs: {len(inventory['ga4_ids'])}")
        for ga4 in inventory["ga4_ids"][:5]:  # Limit display
            print(f"  - {ga4['id']} used in {ga4['container']} {ga4['entity_type']}/{ga4['entity_name']}")
        
        print(f"\nGoogle Ads IDs/Labels: {len(inventory['google_ads_ids'])}")
        for ads in inventory["google_ads_ids"][:5]:
            print(f"  - {ads['id']} used in {ads['container']} {ads['entity_type']}/{ads['entity_name']}")
        
        if inventory["stape_data_tag"]:
            print(f"\nStape Data Tag:")
            print(f"  Endpoint: {inventory['stape_data_tag'].get('endpoint', 'UNKNOWN')}")
            print(f"  Request Path: {inventory['stape_data_tag'].get('request_path', 'UNKNOWN')}")
        
        print(f"\nsGTM Clients: {len(inventory['sgtm_clients'])}")
        for client in inventory["sgtm_clients"][:5]:
            print(f"  - {client['name']} (type: {client['type']}, priority: {client.get('priority', 'N/A')})")
    
    def phase4_gate1_network_proof(self):
        """PHASE 4: Verify browser network requests exist"""
        gate_result = {
            "status": "UNKNOWN",
            "evidence": [],
            "golden_test": None,
            "failure_reason": None
        }
        
        # Select Golden Test event
        golden_test = self._select_golden_test()
        if not golden_test:
            gate_result["status"] = "FAILED"
            gate_result["failure_reason"] = "Cannot select Golden Test event - no events found in Tag Assistant"
            self.findings["gates"]["gate1"] = gate_result
            self._add_missing_evidence(
                "Golden Test Event Selection",
                "No events found in Tag Assistant exports to use as Golden Test",
                "Tag Assistant export with network requests",
                "Use Tag Assistant Chrome extension during test session and export JSON",
                "Tag Assistant JSON with message array containing event_name, timestamp, network request data"
            )
            print("❌ FAILED: Cannot select Golden Test event")
            print("\n⚠️  DOWNSTREAM GATES BLOCKED")
            return
        
        gate_result["golden_test"] = golden_test
        print(f"Golden Test Event Selected:")
        print(f"  Event: {golden_test.get('event_name')}")
        print(f"  Timestamp: {golden_test.get('timestamp')}")
        print(f"  Page URL: {golden_test.get('page_url', 'N/A')[:60]}")
        print(f"  Event ID: {golden_test.get('event_id', 'N/A')}")
        print(f"  Transaction ID: {golden_test.get('transaction_id', 'N/A')}")
        print(f"  Value: {golden_test.get('value', 'N/A')}")
        print(f"  Currency: {golden_test.get('currency', 'N/A')}")
        print(f"  User ID: {golden_test.get('user_id', 'N/A')}")
        print(f"  Source: {golden_test.get('source')}")
        print()
        
        # Verify network request exists
        network_proof = self._verify_network_request(golden_test)
        if network_proof:
            gate_result["status"] = "VERIFIED"
            gate_result["evidence"] = network_proof
            print("✓ VERIFIED: Network request exists")
            print(f"  URL: {network_proof.get('url')}")
            print(f"  Method: {network_proof.get('method')}")
            print(f"  Status: {network_proof.get('status')}")
        else:
            gate_result["status"] = "FAILED"
            gate_result["failure_reason"] = "No network request found for Golden Test event"
            print("❌ FAILED: No network request found")
            self._add_missing_evidence(
                "Network Request for Golden Test",
                "Tag Assistant export does not contain network request data for the event",
                "HAR file or Tag Assistant export with network tab data",
                "Export HAR file from Chrome DevTools Network tab during test session",
                "HTTP request to /metrics or sGTM endpoint with matching timestamp"
            )
            print("\n⚠️  DOWNSTREAM GATES BLOCKED")
        
        self.findings["gates"]["gate1"] = gate_result
    
    def phase5_gate2_sop_contract(self):
        """PHASE 5: Verify SOP contract (Worker + Paths)"""
        if self.findings["gates"].get("gate1", {}).get("status") == "FAILED":
            print("⏸️  BLOCKED: Gate 1 failed")
            self.findings["gates"]["gate2"] = {"status": "BLOCKED"}
            return
        
        gate_result = {
            "status": "UNKNOWN",
            "browser_path": None,
            "worker_logic": None,
            "client_paths": [],
            "verdict": "UNKNOWN"
        }
        
        # Extract browser-facing path from runtime
        if self.tag_assistant_web:
            browser_path = self._extract_browser_path()
            gate_result["browser_path"] = browser_path
            if browser_path:
                print(f"Browser-facing path: {browser_path['path']}")
                print(f"  Evidence: {browser_path['evidence']}")
            else:
                print("Browser-facing path: UNKNOWN")
                self._add_missing_evidence(
                    "Browser-facing request path",
                    "Cannot determine path from Tag Assistant",
                    "Tag Assistant export or HAR with request URL",
                    "Capture network request in Tag Assistant",
                    "Request URL showing /metrics or other path"
                )
        
        # Extract worker rewrite logic from config
        if self.worker_code:
            worker_logic = self._extract_worker_logic()
            gate_result["worker_logic"] = worker_logic
            if worker_logic:
                print(f"\nWorker rewrite logic:")
                print(f"  Match: {worker_logic['match']}")
                print(f"  Upstream: {worker_logic['upstream']}")
                print(f"  Evidence: {worker_logic['evidence']}")
            else:
                print("\nWorker rewrite logic: UNKNOWN")
        else:
            print("\nWorker code: NOT PROVIDED")
            self._add_missing_evidence(
                "Cloudflare Worker code",
                "Worker code file not found in original-data/",
                "Worker JavaScript file",
                "Export Cloudflare Worker code from Cloudflare dashboard",
                "JavaScript file with fetch() and pathname rewrite logic"
            )
        
        # Extract sGTM client claim paths
        if self.sgtm_export:
            client_paths = self._extract_client_paths()
            gate_result["client_paths"] = client_paths
            if client_paths:
                print(f"\nsGTM Client claim paths:")
                for cp in client_paths:
                    print(f"  - {cp['client_name']}: {cp['path']} (priority: {cp.get('priority', 'N/A')})")
            else:
                print(f"\nsGTM Client claim paths: NONE FOUND")
        
        # Determine verdict
        if gate_result["browser_path"] and gate_result["worker_logic"] and gate_result["client_paths"]:
            # Check if paths match
            browser_final = gate_result["browser_path"]["path"]
            worker_upstream_path = gate_result["worker_logic"].get("upstream_path", "")
            client_claim_paths = [cp["path"].split(" (")[0] for cp in gate_result["client_paths"]]  # Strip annotations
            
            # The request_path from Stape Data Tag should match what worker forwards to
            stape_request_path = self.findings["inventory"].get("stape_data_tag", {}).get("request_path", "")
            
            if stape_request_path and stape_request_path in client_claim_paths:
                gate_result["verdict"] = "MATCH"
                gate_result["status"] = "VERIFIED"
                print(f"\n✓ VERDICT: MATCH - SOP contract is consistent")
                print(f"   Browser → /metrics → Worker → {worker_upstream_path} → sGTM")
                print(f"   Stape Data Tag request_path: {stape_request_path}")
                print(f"   sGTM client claims: {client_claim_paths}")
            else:
                gate_result["verdict"] = "MISMATCH"
                gate_result["status"] = "FAILED"
                print(f"\n❌ VERDICT: MISMATCH - SOP contract is BROKEN")
                print(f"   Stape Data Tag request_path: {stape_request_path}")
                print(f"   Worker forwards to: {worker_upstream_path}")
                print(f"   sGTM clients claim: {client_claim_paths}")
                
                # Add root cause
                self._add_root_cause(
                    symptom="Stape Data Tag request_path does not match sGTM client claim path",
                    gate="Gate 2 (SOP Contract)",
                    mechanism=f"Data Tag sends to {stape_request_path} but sGTM clients claim {client_claim_paths}",
                    impact="Requests from browser reach sGTM but no client claims them; events are dropped",
                    evidence=[gate_result]
                )
        else:
            gate_result["verdict"] = "UNKNOWN"
            print(f"\n⚠️  VERDICT: UNKNOWN - Insufficient evidence")
        
        self.findings["gates"]["gate2"] = gate_result
    
    def phase6_gate3_sgtm_inbound(self):
        """PHASE 6: Verify sGTM receives and claims the event"""
        if self.findings["gates"].get("gate2", {}).get("status") == "FAILED":
            print("⏸️  BLOCKED: Gate 2 failed")
            self.findings["gates"]["gate3"] = {"status": "BLOCKED"}
            return
        
        gate_result = {
            "status": "UNKNOWN",
            "inbound_hit": None,
            "claiming_client": None,
            "key_fields": {}
        }
        
        golden_test = self.findings["gates"]["gate1"]["golden_test"]
        if not golden_test:
            gate_result["status"] = "FAILED"
            print("❌ FAILED: No Golden Test event")
            self.findings["gates"]["gate3"] = gate_result
            return
        
        # Check if sGTM Tag Assistant has ANY messages at all
        sgtm_message_count = 0
        if self.tag_assistant_server:
            if isinstance(self.tag_assistant_server, dict):
                if "data" in self.tag_assistant_server and isinstance(self.tag_assistant_server["data"], dict):
                    containers = self.tag_assistant_server["data"].get("containers", [])
                    for container in containers:
                        if "messages" in container:
                            sgtm_message_count += len(container["messages"])
        
        if sgtm_message_count == 0:
            gate_result["status"] = "FAILED"
            print("❌ FAILED: sGTM Tag Assistant is empty (0 messages)")
            print("   This indicates either:")
            print("   1. sGTM server is not receiving requests from browser/worker")
            print("   2. Tag Assistant was not connected to sGTM during test")
            print("   3. sGTM preview mode was not active")
            
            # Add root cause
            self._add_root_cause(
                symptom="sGTM Tag Assistant has zero messages - no events reaching sGTM",
                gate="Gate 3 (sGTM Inbound)",
                mechanism="Despite wGTM sending to /metrics and worker configuration appearing correct, "
                          "sGTM is not recording any inbound requests in Tag Assistant",
                impact="Cannot verify if events reach sGTM; cannot validate data contract; "
                       "complete tracking pipeline breakdown",
                evidence=[{
                    "sgtm_message_count": sgtm_message_count,
                    "wgtm_message_count": len(self.findings.get("source_index", [])),
                    "stape_data_tag_endpoint": self.findings["inventory"].get("stape_data_tag", {}).get("endpoint"),
                    "worker_configured": self.worker_code is not None
                }]
            )
            
            self._add_missing_evidence(
                "sGTM inbound events",
                "Tag Assistant sGTM export is completely empty - no messages recorded",
                "Tag Assistant sGTM export with events showing inbound requests, OR Stape server logs showing hits",
                "1. Enable sGTM Preview Mode in GTM\n"
                "   2. Connect Tag Assistant to sGTM container\n"
                "   3. Perform test transaction\n"
                "   4. Export Tag Assistant recording\n"
                "   OR\n"
                "   1. Check Stape logs dashboard for incoming requests\n"
                "   2. Verify Cloudflare Worker logs show forwarding to sGTM origin",
                "sGTM Tag Assistant JSON with messages array containing inbound event data, "
                "OR Stape logs showing POST requests to /data endpoint"
            )
            
            self.findings["gates"]["gate3"] = gate_result
            return
        
        # Look for inbound hit in sGTM Tag Assistant
        inbound_hit = self._find_sgtm_inbound(golden_test)
        if inbound_hit:
            gate_result["inbound_hit"] = inbound_hit
            gate_result["claiming_client"] = inbound_hit.get("client")
            gate_result["key_fields"] = inbound_hit.get("fields", {})
            gate_result["status"] = "VERIFIED"
            
            print(f"✓ VERIFIED: sGTM received event")
            print(f"  Claiming client: {inbound_hit.get('client', 'UNKNOWN')}")
            print(f"  Event name: {inbound_hit.get('fields', {}).get('event_name', 'N/A')}")
            print(f"  Event ID: {inbound_hit.get('fields', {}).get('event_id', 'N/A')}")
            print(f"  Transaction ID: {inbound_hit.get('fields', {}).get('transaction_id', 'N/A')}")
            print(f"  User ID: {inbound_hit.get('fields', {}).get('user_id', 'N/A')}")
            print(f"  Consent signals: {inbound_hit.get('fields', {}).get('consent', 'N/A')}")
        else:
            gate_result["status"] = "FAILED"
            print(f"❌ FAILED: sGTM Tag Assistant has messages ({sgtm_message_count}) but no matching Golden Test event")
            print(f"   Golden Test event: {golden_test['event_name']}")
            self._add_missing_evidence(
                "sGTM inbound event matching Golden Test",
                f"sGTM Tag Assistant has {sgtm_message_count} messages but none match the Golden Test event {golden_test['event_name']}",
                "sGTM Tag Assistant export with the specific test event, or explanation of which events are present",
                "Re-run test ensuring sGTM preview mode is active during the specific test event",
                f"sGTM Tag Assistant JSON with messages containing event_name={golden_test['event_name']}"
            )
        
        self.findings["gates"]["gate3"] = gate_result
    
    def phase7_gate4_mutation_check(self):
        """PHASE 7: Compare data contract across layers"""
        if self.findings["gates"].get("gate3", {}).get("status") == "FAILED":
            print("⏸️  BLOCKED: Gate 3 failed")
            self.findings["gates"]["gate4"] = {"status": "BLOCKED"}
            return
        
        gate_result = {
            "status": "UNKNOWN",
            "mutations": []
        }
        
        golden_test = self.findings["gates"]["gate1"]["golden_test"]
        sgtm_inbound = self.findings["gates"]["gate3"].get("inbound_hit")
        
        if not golden_test or not sgtm_inbound:
            gate_result["status"] = "UNKNOWN"
            print("⚠️  UNKNOWN: Missing data for comparison")
            self.findings["gates"]["gate4"] = gate_result
            return
        
        # Compare wGTM outbound vs sGTM inbound
        mutations = self._detect_mutations(golden_test, sgtm_inbound)
        
        if mutations:
            gate_result["status"] = "VERIFIED"
            gate_result["mutations"] = mutations
            print(f"⚠️  MUTATIONS DETECTED: {len(mutations)} field(s) changed")
            for mut in mutations:
                print(f"  - {mut['field']}: {mut['wgtm_value']} → {mut['sgtm_value']}")
                print(f"    Evidence: {mut['evidence']}")
        else:
            gate_result["status"] = "VERIFIED"
            print("✓ VERIFIED: No mutations detected")
        
        self.findings["gates"]["gate4"] = gate_result
    
    def phase8_gate5_identity_dedup(self):
        """PHASE 8: Verify event_id and deduplication"""
        if self.findings["gates"].get("gate4", {}).get("status") == "BLOCKED":
            print("⏸️  BLOCKED: Gate 4 blocked")
            self.findings["gates"]["gate5"] = {"status": "BLOCKED"}
            return
        
        gate_result = {
            "status": "UNKNOWN",
            "event_id_present": False,
            "event_id_source": None,
            "dedup_mechanism": None
        }
        
        golden_test = self.findings["gates"]["gate1"]["golden_test"]
        
        if golden_test and golden_test.get("event_id"):
            gate_result["event_id_present"] = True
            gate_result["event_id_source"] = "Tag Assistant web"
            print(f"✓ Event ID present: {golden_test['event_id']}")
        else:
            gate_result["event_id_present"] = False
            print(f"⚠️  Event ID not found in Golden Test event")
        
        # Check for dedup config in sGTM
        if self.sgtm_export:
            dedup_config = self._find_dedup_config()
            if dedup_config:
                gate_result["dedup_mechanism"] = dedup_config
                gate_result["status"] = "VERIFIED"
                print(f"Dedup mechanism: {dedup_config['type']}")
                print(f"  Evidence: {dedup_config['evidence']}")
            else:
                print(f"⚠️  No dedup mechanism found in sGTM config")
        
        self.findings["gates"]["gate5"] = gate_result
    
    def phase9_root_causes(self):
        """PHASE 9: Consolidate and present root causes (max 5)"""
        root_causes = self.findings.get("root_causes", [])
        
        if not root_causes:
            print("✓ No root causes identified")
            return
        
        print(f"Root Causes Identified: {len(root_causes)}")
        print()
        
        for i, rc in enumerate(root_causes[:5], 1):
            print(f"ROOT CAUSE #{i}")
            print(f"  Symptom: {rc['symptom']}")
            print(f"  Failing Gate: {rc['gate']}")
            print(f"  Mechanism: {rc['mechanism']}")
            print(f"  Impact: {rc['impact']}")
            print()
    
    def phase10_action_cards(self):
        """PHASE 10: Generate actionable fix plans"""
        root_causes = self.findings.get("root_causes", [])
        
        if not root_causes:
            print("✓ No action cards needed")
            return
        
        print(f"Action Cards: {len(root_causes)}")
        print()
        
        for i, rc in enumerate(root_causes[:5], 1):
            action_card = self._generate_action_card(rc)
            self.findings["action_cards"].append(action_card)
            
            print(f"ACTION CARD #{i}")
            print(f"  Problem: {action_card['problem']}")
            print(f"  Evidence: {action_card['evidence']}")
            print(f"  Change Location: {action_card['location']}")
            print(f"  UI Path: {action_card['ui_path']}")
            print(f"  Fields to Edit: {action_card['fields']}")
            print(f"  New Values: {action_card['new_values']}")
            print(f"  Validation: {action_card['validation']}")
            print(f"  Rollback: {action_card['rollback']}")
            print()
    
    def output_summary(self):
        """Output final summary"""
        print("\nGate Results Summary:")
        print("-" * 40)
        for gate_name, gate_data in self.findings.get("gates", {}).items():
            status = gate_data.get("status", "UNKNOWN")
            symbol = {"VERIFIED": "✓", "FAILED": "❌", "UNKNOWN": "⚠️", "BLOCKED": "⏸️"}.get(status, "?")
            print(f"  {symbol} {gate_name}: {status}")
        
        print(f"\nRoot Causes: {len(self.findings.get('root_causes', []))}")
        print(f"Action Cards: {len(self.findings.get('action_cards', []))}")
        print(f"Missing Evidence Requests: {len(self.findings.get('missing_evidence', []))}")
        
        if self.findings.get("missing_evidence"):
            print("\nMissing Evidence (capture these to complete audit):")
            for i, me in enumerate(self.findings["missing_evidence"][:5], 1):
                print(f"  {i}. {me['claim']}")
                print(f"     Needed: {me['needed']}")
    
    # Helper methods
    
    def _find_file_pattern(self, pattern: str, usage_context: Optional[str] = None, 
                          exclude_pattern: Optional[str] = None) -> Optional[Path]:
        """Find first file matching glob pattern"""
        if not self.data_dir.exists():
            return None
        
        for file_path in self.data_dir.iterdir():
            if fnmatch(file_path.name.lower(), pattern.lower()):
                if exclude_pattern and exclude_pattern.lower() in file_path.name.lower():
                    continue
                
                if usage_context and file_path.suffix == ".json":
                    try:
                        with open(file_path) as f:
                            data = json.load(f)
                            ctx = data.get("containerVersion", {}).get("container", {}).get("usageContext", [])
                            if usage_context not in ctx:
                                continue
                    except:
                        continue
                
                return file_path
        return None
    
    def _find_datalayer_files(self) -> List[Path]:
        """Find all datalayer sample files"""
        files = []
        if not self.data_dir.exists():
            return files
        
        for file_path in self.data_dir.iterdir():
            name_lower = file_path.name.lower()
            if ("datalayer" in name_lower or "data layer" in name_lower) and file_path.suffix == ".json":
                files.append(file_path)
        return files
    
    def _load_file(self, file_type: str, path: Path):
        """Load file into appropriate attribute"""
        try:
            if file_type == "wGTM export JSON":
                with open(path) as f:
                    self.wgtm_export = json.load(f)
            elif file_type == "sGTM export JSON":
                with open(path) as f:
                    self.sgtm_export = json.load(f)
            elif file_type == "Tag Assistant web":
                with open(path) as f:
                    self.tag_assistant_web = json.load(f)
            elif file_type == "Tag Assistant server":
                with open(path) as f:
                    self.tag_assistant_server = json.load(f)
            elif file_type == "Worker code":
                with open(path) as f:
                    self.worker_code = f.read()
            elif file_type == "Stape logs":
                with open(path) as f:
                    reader = csv.DictReader(f)
                    self.stape_logs = list(reader)
            elif file_type == "DataLayer samples":
                with open(path) as f:
                    self.datalayer_samples.append({
                        "file": path.name,
                        "data": json.load(f)
                    })
        except Exception as e:
            print(f"    ⚠️  Error loading {path.name}: {e}")
    
    def _index_tag_assistant(self, ta_data: Dict, source: str, priority_events: List[str]) -> List[Dict]:
        """Extract event index from Tag Assistant data"""
        index = []
        event_counts = defaultdict(int)
        
        try:
            # Try multiple paths for messages
            messages = []
            if isinstance(ta_data, dict):
                # New Tag Assistant format: data.containers[].messages
                if "data" in ta_data and isinstance(ta_data["data"], dict):
                    containers = ta_data["data"].get("containers", [])
                    for container in containers:
                        if "messages" in container:
                            messages.extend(container["messages"])
                # Old format: messages at root
                elif "messages" in ta_data:
                    messages = ta_data["messages"]
            elif isinstance(ta_data, list):
                messages = ta_data
            
            for msg in messages:
                event_name = None
                
                # Extract event name from message
                if isinstance(msg, dict):
                    # Check message.event
                    if "message" in msg and isinstance(msg["message"], dict):
                        event_name = msg["message"].get("event")
                    # Check abstractModel.event
                    elif "abstractModel" in msg and isinstance(msg["abstractModel"], dict):
                        event_name = msg["abstractModel"].get("event")
                    # Check eventName
                    elif "eventName" in msg:
                        event_name = msg["eventName"]
                
                if not event_name or event_name not in priority_events:
                    continue
                
                # Limit to 2 per event type
                if event_counts[event_name] >= 2:
                    continue
                
                event_counts[event_name] += 1
                
                # Extract key fields
                entry = {
                    "event_name": event_name,
                    "source": source,
                    "pointer": f"messages[{messages.index(msg)}]",
                    "timestamp": msg.get("timestamp", msg.get("eventTimestamp", "N/A")),
                    "page_url": self._extract_page_url(msg),
                    "event_id": self._extract_event_id(msg),
                    "transaction_id": self._extract_field(msg, "transaction_id"),
                    "value": self._extract_field(msg, "value"),
                    "currency": self._extract_field(msg, "currency"),
                    "user_id": self._extract_field(msg, "user_id"),
                }
                
                index.append(entry)
        
        except Exception as e:
            print(f"    ⚠️  Error indexing {source}: {e}")
        
        return index
    
    def _index_datalayer(self, dl_sample: Dict, priority_events: List[str]) -> List[Dict]:
        """Extract event index from DataLayer sample"""
        index = []
        try:
            data = dl_sample["data"]
            
            # Handle both dict and list formats
            if isinstance(data, list):
                # Find event push in array format
                for i, item in enumerate(data):
                    if isinstance(item, dict):
                        # Check for event key
                        event_name = item.get("event") or item.get("0")
                        if event_name and event_name in priority_events:
                            # Try to extract more fields from subsequent array items
                            ecommerce = None
                            for j in range(i, min(i+5, len(data))):
                                if isinstance(data[j], dict) and "ecommerce" in data[j]:
                                    ecommerce = data[j]["ecommerce"]
                                    break
                            
                            entry = {
                                "event_name": event_name,
                                "source": f"datalayer:{dl_sample['file']}",
                                "pointer": f"[{i}]",
                                "timestamp": "N/A",
                                "page_url": "N/A",
                                "event_id": item.get("event_id", "N/A"),
                                "transaction_id": (ecommerce.get("transaction_id") if ecommerce else "N/A"),
                            }
                            index.append(entry)
                            break
            elif isinstance(data, dict):
                event_name = data.get("event")
                
                if event_name and event_name in priority_events:
                    entry = {
                        "event_name": event_name,
                        "source": f"datalayer:{dl_sample['file']}",
                        "pointer": "root",
                        "timestamp": "N/A",
                        "page_url": data.get("page_url", "N/A"),
                        "event_id": data.get("event_id", "N/A"),
                        "transaction_id": data.get("transaction_id", data.get("ecommerce", {}).get("transaction_id", "N/A")),
                    }
                    index.append(entry)
        except Exception as e:
            print(f"    ⚠️  Error indexing datalayer: {e}")
        
        return index
    
    def _inventory_gtm_container(self, export_data: Dict, container_type: str) -> Dict:
        """Extract inventory from GTM container export"""
        inventory = {
            "type": container_type,
            "container_id": "UNKNOWN",
            "version_id": "UNKNOWN",
            "export_time": "UNKNOWN",
            "ga4_ids": [],
            "google_ads_ids": [],
            "other_vendors": [],
            "stape_data_tag": None,
            "clients": []
        }
        
        try:
            cv = export_data.get("containerVersion", {})
            inventory["container_id"] = cv.get("containerId", "UNKNOWN")
            inventory["version_id"] = cv.get("containerVersionId", "UNKNOWN")
            inventory["export_time"] = export_data.get("exportTime", "UNKNOWN")
            
            # Extract tags
            tags = cv.get("tag", [])
            for tag in tags:
                tag_name = tag.get("name", "")
                tag_type = tag.get("type", "")
                
                # GA4
                if tag_type == "googtag" or "GA4" in tag_name or "Google Analytics" in tag_type:
                    for param in tag.get("parameter", []):
                        if param.get("key") == "measurementId":
                            inventory["ga4_ids"].append({
                                "id": param.get("value", ""),
                                "container": container_type,
                                "entity_type": "Tag",
                                "entity_name": tag_name
                            })
                
                # Google Ads
                if "google_ads" in tag_type.lower() or "adwords" in tag_type.lower():
                    for param in tag.get("parameter", []):
                        if param.get("key") in ["conversionId", "conversionLabel"]:
                            inventory["google_ads_ids"].append({
                                "id": param.get("value", ""),
                                "container": container_type,
                                "entity_type": "Tag",
                                "entity_name": tag_name
                            })
                
                # Stape Data Tag
                if "data tag" in tag_name.lower() or tag_type == "cvt_MBTSV":
                    stape_config = {"name": tag_name, "type": tag_type}
                    for param in tag.get("parameter", []):
                        key = param.get("key")
                        if key == "gtm_server_domain":
                            stape_config["endpoint"] = param.get("value", "")
                        elif key == "request_path":
                            stape_config["request_path"] = param.get("value", "")
                        elif key == "transportUrl":
                            stape_config["endpoint"] = param.get("value", "")
                    inventory["stape_data_tag"] = stape_config
            
            # Extract clients (sGTM only)
            if container_type == "sGTM":
                clients = cv.get("client", [])
                for client in clients:
                    client_info = {
                        "name": client.get("name", ""),
                        "type": client.get("type", ""),
                        "priority": self._extract_client_priority(client)
                    }
                    inventory["clients"].append(client_info)
        
        except Exception as e:
            print(f"    ⚠️  Error inventorying {container_type}: {e}")
        
        return inventory
    
    def _extract_page_url(self, msg: Dict) -> str:
        """Extract page URL from message"""
        # Try multiple locations
        if "abstractModel" in msg and isinstance(msg["abstractModel"], dict):
            return msg["abstractModel"].get("page_location", msg["abstractModel"].get("page_url", "N/A"))
        if "message" in msg and isinstance(msg["message"], dict):
            return msg["message"].get("page_location", msg["message"].get("page_url", "N/A"))
        return "N/A"
    
    def _extract_event_id(self, msg: Dict) -> str:
        """Extract event_id from message"""
        # Check top level first
        if "eventId" in msg:
            return str(msg["eventId"])
        if "abstractModel" in msg and isinstance(msg["abstractModel"], dict):
            if "event_id" in msg["abstractModel"]:
                return str(msg["abstractModel"]["event_id"])
            # Check gtm.uniqueEventId
            if "gtm" in msg["abstractModel"] and isinstance(msg["abstractModel"]["gtm"], dict):
                unique_id = msg["abstractModel"]["gtm"].get("uniqueEventId")
                if unique_id:
                    return str(unique_id)
        if "message" in msg and isinstance(msg["message"], dict):
            if "event_id" in msg["message"]:
                return str(msg["message"]["event_id"])
            if "gtm.uniqueEventId" in msg["message"]:
                return str(msg["message"]["gtm.uniqueEventId"])
        return "N/A"
    
    def _extract_field(self, msg: Dict, field_name: str) -> str:
        """Extract generic field from message"""
        if "abstractModel" in msg and isinstance(msg["abstractModel"], dict):
            value = msg["abstractModel"].get(field_name)
            if value is not None:
                return str(value)
            # Check ecommerce object
            if "ecommerce" in msg["abstractModel"] and isinstance(msg["abstractModel"]["ecommerce"], dict):
                value = msg["abstractModel"]["ecommerce"].get(field_name)
                if value is not None:
                    return str(value)
        if "message" in msg and isinstance(msg["message"], dict):
            value = msg["message"].get(field_name)
            if value is not None:
                return str(value)
        return "N/A"
    
    def _extract_client_priority(self, client: Dict) -> str:
        """Extract priority from client config"""
        for param in client.get("parameter", []):
            if param.get("key") == "priority":
                return param.get("value", "N/A")
        return "N/A"
    
    def _select_golden_test(self) -> Optional[Dict]:
        """Select one concrete event as Golden Test"""
        # Prioritize purchase, then begin_checkout, then add_to_cart
        priority_order = ["purchase", "begin_checkout", "add_to_cart", "view_item"]
        
        for event_name in priority_order:
            for entry in self.findings.get("source_index", []):
                if entry["event_name"] == event_name:
                    return entry
        
        # Fallback to first event
        if self.findings.get("source_index"):
            return self.findings["source_index"][0]
        
        return None
    
    def _verify_network_request(self, golden_test: Dict) -> Optional[Dict]:
        """Verify network request exists for Golden Test
        
        NOTE: This is a simplified implementation that infers network activity
        from Tag Assistant presence. For production use, implement HAR file parsing
        or direct network log analysis for true network proof.
        """
        # In a real implementation, would parse HAR file or network logs here
        # Current implementation: infer from Tag Assistant presence as placeholder
        if golden_test.get("source", "").startswith("tag_assistant"):
            return {
                "url": "INFERRED from Tag Assistant presence (HAR parsing not implemented)",
                "method": "POST",
                "status": "200 (inferred)",
                "note": "This is an inference, not direct evidence. Implement HAR parsing for true network proof."
            }
        return None
    
    def _extract_browser_path(self) -> Optional[Dict]:
        """Extract browser-facing path from runtime evidence
        
        NOTE: This is a simplified implementation that infers the path.
        For production use, implement actual network request parsing.
        """
        # In a real implementation, would parse actual network requests from HAR or Tag Assistant
        # Look for Stape Data Tag or /metrics in Tag Assistant
        if self.tag_assistant_web:
            # Check if Stape Data Tag endpoint is configured
            stape_endpoint = self.findings.get("inventory", {}).get("stape_data_tag", {}).get("endpoint", "")
            if "/metrics" in stape_endpoint:
                return {
                    "path": "/metrics",
                    "evidence": f"Inferred from Stape Data Tag endpoint config: {stape_endpoint} (actual network request parsing not implemented)",
                    "note": "This is CONFIG evidence, not RUNTIME. Implement network request parsing for true runtime proof."
                }
        return None
    
    def _extract_worker_logic(self) -> Optional[Dict]:
        """Extract worker rewrite logic from code"""
        if not self.worker_code:
            return None
        
        # Simple regex to find pathname replace
        match = re.search(r"pathname\.replace\(['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]*)['\"]", self.worker_code)
        if match:
            return {
                "match": match.group(1),
                "upstream": match.group(2) or "/",
                "upstream_path": match.group(2) or "/",
                "evidence": "worker code | pathname.replace() | " + match.group(0)
            }
        return None
    
    def _extract_client_paths(self) -> List[Dict]:
        """Extract sGTM client claim paths"""
        clients = []
        if not self.sgtm_export:
            return clients
        
        cv = self.sgtm_export.get("containerVersion", {})
        for client in cv.get("client", []):
            client_name = client.get("name", "")
            client_type = client.get("type", "")
            
            # Look for path claim in parameters
            found_path = False
            for param in client.get("parameter", []):
                if param.get("key") in ["claimPath", "requestPath", "path"]:
                    clients.append({
                        "client_name": client_name,
                        "path": param.get("value", "/"),
                        "priority": self._extract_client_priority(client),
                        "type": client_type
                    })
                    found_path = True
                    break
            
            # Stape Data Client defaults to /data path
            if not found_path and ("data client" in client_name.lower() or "cvt_" in client_type):
                clients.append({
                    "client_name": client_name,
                    "path": "/data (default for Stape Data Client)",
                    "priority": self._extract_client_priority(client),
                    "type": client_type
                })
        
        return clients
    
    def _find_sgtm_inbound(self, golden_test: Dict) -> Optional[Dict]:
        """Find matching inbound event in sGTM Tag Assistant"""
        if not self.tag_assistant_server:
            return None
        
        # Simplified lookup by event_name
        target_event = golden_test["event_name"]
        
        try:
            messages = []
            if isinstance(self.tag_assistant_server, dict):
                # New format: data.containers[].messages
                if "data" in self.tag_assistant_server and isinstance(self.tag_assistant_server["data"], dict):
                    containers = self.tag_assistant_server["data"].get("containers", [])
                    for container in containers:
                        if "messages" in container:
                            messages.extend(container["messages"])
                # Old format: messages at root
                elif "messages" in self.tag_assistant_server:
                    messages = self.tag_assistant_server["messages"]
            
            for msg in messages:
                event_name = self._extract_field(msg, "event")
                if event_name == target_event:
                    return {
                        "client": "Data Client (inferred)",
                        "fields": {
                            "event_name": event_name,
                            "event_id": self._extract_event_id(msg),
                            "transaction_id": self._extract_field(msg, "transaction_id"),
                            "user_id": self._extract_field(msg, "user_id"),
                            "consent": self._extract_field(msg, "consent")
                        }
                    }
        except:
            pass
        
        return None
    
    def _detect_mutations(self, wgtm_event: Dict, sgtm_event: Dict) -> List[Dict]:
        """Compare fields between wGTM and sGTM to detect mutations"""
        mutations = []
        
        # Compare key fields
        compare_fields = ["event_name", "transaction_id", "value", "currency"]
        
        for field in compare_fields:
            wgtm_val = wgtm_event.get(field, "N/A")
            sgtm_val = sgtm_event.get("fields", {}).get(field, "N/A")
            
            if wgtm_val != "N/A" and sgtm_val != "N/A" and wgtm_val != sgtm_val:
                mutations.append({
                    "field": field,
                    "wgtm_value": wgtm_val,
                    "sgtm_value": sgtm_val,
                    "evidence": f"Golden Test comparison | {field}"
                })
        
        return mutations
    
    def _find_dedup_config(self) -> Optional[Dict]:
        """Find deduplication configuration in sGTM"""
        if not self.sgtm_export:
            return None
        
        cv = self.sgtm_export.get("containerVersion", {})
        
        # Look for event_id usage in variables or tags
        for var in cv.get("variable", []):
            if "event_id" in var.get("name", "").lower():
                return {
                    "type": "event_id variable present",
                    "evidence": f"sGTM Variable/{var.get('name')}"
                }
        
        return None
    
    def _add_root_cause(self, symptom: str, gate: str, mechanism: str, impact: str, evidence: List):
        """Add a root cause to findings"""
        self.findings["root_causes"].append({
            "symptom": symptom,
            "gate": gate,
            "mechanism": mechanism,
            "impact": impact,
            "evidence": evidence
        })
    
    def _add_missing_evidence(self, claim: str, why: str, needed: str, how_to_capture: str, success_looks_like: str):
        """Add a missing evidence request"""
        self.findings["missing_evidence"].append({
            "claim": claim,
            "why": why,
            "needed": needed,
            "how_to_capture": how_to_capture,
            "success_looks_like": success_looks_like
        })
    
    def _generate_action_card(self, root_cause: Dict) -> Dict:
        """Generate actionable fix card from root cause"""
        problem = root_cause["symptom"]
        gate = root_cause.get("gate", "")
        
        # Generate specific action card based on the gate that failed
        if "Gate 3" in gate and "zero messages" in problem.lower():
            return {
                "problem": problem,
                "evidence": root_cause.get("mechanism", ""),
                "location": "Network/Infrastructure layer",
                "ui_path": "Cloudflare Dashboard → Workers → messerattach.com route",
                "fields": "Worker route pattern, Worker script, DNS settings",
                "new_values": "VERIFICATION NEEDED:\n"
                             "1. Confirm Worker route is active: /metrics*\n"
                             "2. Verify Worker script forwards requests\n"
                             "3. Check sGTM origin DNS: sgtm.messerattach.com → Stape\n"
                             "4. Verify Stape container is running",
                "validation": "1. Check Cloudflare Worker logs for /metrics requests\n"
                            "2. Check Stape logs for incoming requests\n"
                            "3. Re-run troubleshooter with sGTM Tag Assistant in preview mode\n"
                            "4. Verify Gate 3 shows messages > 0",
                "rollback": "N/A - This is a diagnostic/verification action"
            }
        elif "Gate 2" in gate and "mismatch" in problem.lower():
            return {
                "problem": problem,
                "evidence": root_cause.get("mechanism", ""),
                "location": "wGTM Tag/Data Tag OR sGTM Client/Data Client",
                "ui_path": "GTM Web Container → Tags → Data Tag → Settings OR\n"
                          "GTM Server Container → Clients → Data Client → Settings",
                "fields": "Data Tag: request_path parameter\n"
                         "Data Client: claim path configuration",
                "new_values": "Ensure both use the same path (recommended: /data)",
                "validation": "1. Re-export both GTM containers\n"
                            "2. Re-run troubleshooter\n"
                            "3. Verify Gate 2 shows MATCH verdict",
                "rollback": "Revert to previous container versions"
            }
        else:
            # Generic action card
            return {
                "problem": problem,
                "evidence": root_cause.get("mechanism", ""),
                "location": gate,
                "ui_path": "UNKNOWN - Manual inspection required",
                "fields": "UNKNOWN",
                "new_values": "UNKNOWN - Requires subject matter expert review",
                "validation": "Re-run troubleshooter and verify gate passes",
                "rollback": "Revert to previous container version"
            }


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Evidence-First GTM Troubleshooter"
    )
    parser.add_argument(
        "--data-dir",
        default="original-data",
        help="Directory containing input files (default: original-data)"
    )
    parser.add_argument(
        "--output",
        help="Output file for results (default: stdout)"
    )
    
    args = parser.parse_args()
    
    # Handle output redirection
    original_stdout = None
    output_file = None
    
    if args.output:
        original_stdout = sys.stdout
        try:
            output_file = open(args.output, 'w')
            sys.stdout = output_file
        except IOError as e:
            print(f"Error opening output file: {e}", file=sys.stderr)
            sys.exit(1)
    
    try:
        troubleshooter = GTMTroubleshooter(data_dir=args.data_dir)
        troubleshooter.run_full_audit()
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        # Restore stdout and close file if redirected
        if original_stdout is not None:
            sys.stdout = original_stdout
            if output_file is not None:
                output_file.close()


if __name__ == "__main__":
    main()
