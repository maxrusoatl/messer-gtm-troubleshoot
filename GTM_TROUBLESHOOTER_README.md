# Evidence-First GTM Troubleshooter

## Overview

This tool implements an **evidence-first, fail-closed** troubleshooting methodology for server-side tracking pipelines using:
- WooCommerce
- Web Google Tag Manager (wGTM)
- Server-side Google Tag Manager (sGTM) via Stape
- Cloudflare Same-Origin Proxy (SOP) Worker
- Complianz Consent Mode v2

**Key Principles:**
- ✅ Every claim must have evidence (file | pointer | snippet)
- ✅ Evidence is labeled [RUNTIME] or [CONFIG]
- ✅ If data is missing or unproven, it's a STOP condition (fail closed)
- ✅ No speculation - only evidence-backed diagnoses
- ✅ Gates fail sequentially - upstream failures block downstream analysis

## Installation

### Prerequisites
- Python 3.7+
- No external dependencies required (uses only Python standard library)

### Setup
```bash
# Clone or copy the script
cd /home/runner/work/messer-gtm-troubleshoot/messer-gtm-troubleshoot

# Make executable (optional)
chmod +x gtm_troubleshooter.py

# Run
python3 gtm_troubleshooter.py
```

## Usage

### Basic Usage
```bash
# Run with default data directory (original-data/)
python3 gtm_troubleshooter.py

# Specify custom data directory
python3 gtm_troubleshooter.py --data-dir /path/to/data

# Save output to file
python3 gtm_troubleshooter.py --output report.txt
```

### Data Directory Structure

Place your evidence files in `original-data/` (or specified directory):

#### Required Files
- **wGTM Export**: `GTM-*_workspace*.json` (with usageContext: WEB)
- **sGTM Export**: `GTM-*_workspace*.json` (with usageContext: SERVER)
- **Tag Assistant Web**: `tag_assistant_*messerattach*.json` (browser-side recording)
- **Tag Assistant Server**: `tag_assistant_sgtm_*.json` (server-side recording)

#### Optional Files (Recommended)
- **Stape Logs**: `*stape*logs*.csv`
- **Worker Code**: `*worker*.js` (Cloudflare Worker script)
- **Cloudflare Notes**: `*cloudflare*.md`
- **DataLayer Samples**: `*datalayer*.json`, `*data layer*.json`
- **Plugin Settings**: `STAPE_SGTM_PLUGIN_SETTINGS.md`
- **WP Rocket Settings**: `*rocket*.md`

## Workflow (10 Phases)

### Phase 1: Coverage Summary
Discovers and categorizes all available input files.

**Output:** List of found vs. missing artifacts

### Phase 2: Source Index
Builds an evidence map for key events (view_item, add_to_cart, begin_checkout, purchase, etc.)

**Output:** Table showing event_name, timestamp, page_url, event_id, transaction_id, source

**Limit:** Max 2 entries per event type per source

### Phase 3: Inventory (CONFIG)
Extracts configuration from GTM containers:
- Container versions and IDs
- GA4 Measurement IDs
- Google Ads IDs/labels
- Stape Data Tag endpoint + request_path
- sGTM client configurations
- Other vendor tags (Meta, UET, LinkedIn, etc.)

**Output:** Inventory table with evidence sources

### Phase 4: Gate 1 - Browser Network Proof [RUNTIME]
**Goal:** Prove browser actually sends the request (Preview ≠ Send)

**Selects a Golden Test Event:** One concrete event instance used throughout analysis

**Verifies:**
- Network request exists for Golden Test
- Request URL, method, status code

**Status:** VERIFIED / FAILED / UNKNOWN

**If FAILED:** All downstream gates are BLOCKED

### Phase 5: Gate 2 - SOP Contract [CONFIG]
**Goal:** Verify the 3-line SOP contract is consistent

**Checks:**
1. Browser-facing path (e.g., `/metrics`)
2. Worker rewrite logic (e.g., `/metrics/` → `/`)
3. sGTM client claim paths (e.g., Data Client claims `/data`)

**Verdict:** MATCH / MISMATCH / UNKNOWN

**If MISMATCH:** FAILED - requests won't be claimed by sGTM client

### Phase 6: Gate 3 - sGTM Claim + Inbound eventData [RUNTIME]
**Goal:** Prove sGTM receives and claims the event

**Checks:**
- sGTM Tag Assistant has messages
- Inbound hit exists for Golden Test
- Client claims the request
- Key fields present: event_name, event_id, transaction_id, user_id, consent

**Special Case:** If sGTM Tag Assistant is completely empty (0 messages), this indicates a critical infrastructure issue.

**Status:** VERIFIED / FAILED / BLOCKED

### Phase 7: Gate 4 - Data Contract + Mutation Check [RUNTIME]
**Goal:** Detect field-level mutations across layers

**Compares:**
- wGTM outbound payload vs sGTM inbound eventData
- Key fields: event_name, transaction_id, value, currency, user_id

**Output:** List of detected mutations with evidence

### Phase 8: Gate 5 - Identity + Dedup [RUNTIME + CONFIG]
**Goal:** Verify event_id generation and deduplication

**Checks:**
- event_id present and source
- Dedup mechanism configured (sGTM store / platform / none)
- Correlation rules for duplicate detection

### Phase 9: Root Causes (Max 5)
Consolidates findings into root causes, each with:
- Symptom [RUNTIME]
- Failing gate/layer
- Mechanism [CONFIG + RUNTIME]
- Impact (strictly derived, no speculation)

### Phase 10: Fix Plan (Action Cards)
For each root cause, generates an Action Card:
- Problem statement
- Evidence reference
- Exact change location (entity name)
- UI path (click path in GTM/Cloudflare)
- Fields to edit
- New values (or UNKNOWN if evidence insufficient)
- Validation steps (exact artifacts + success criteria)
- Rollback steps

## Output Format

### Gate Results Summary
```
Gate Results Summary:
----------------------------------------
  ✓ gate1: VERIFIED
  ✓ gate2: VERIFIED
  ❌ gate3: FAILED
  ⏸️ gate4: BLOCKED
  ⏸️ gate5: BLOCKED
```

### Symbols
- ✓ VERIFIED - Gate passed with evidence
- ❌ FAILED - Gate failed with evidence of failure
- ⚠️ UNKNOWN - Insufficient evidence to determine
- ⏸️ BLOCKED - Upstream gate failed, cannot evaluate

### Missing Evidence Requests
When evidence is insufficient, the tool outputs EVIDENCE NEEDED cards:
- Unknown claim
- Why it cannot be proven
- Needed artifact (specific file/data)
- How to capture (step-by-step)
- What success evidence looks like

## Evidence Standards

### Evidence Reference Format
Every claim includes: `[TYPE] file | pointer | "snippet"`

**Example:**
```
[CONFIG] GTM-MNRP4PF_workspace253.json | containerVersion.tag[5].parameter[2] | "request_path: /data"
[RUNTIME] tag_assistant_web | messages[47] | "event: purchase, value: 1.00"
```

### Evidence Types
- **[CONFIG]** - Static configuration (GTM exports, worker code, settings files)
- **[RUNTIME]** - Actual execution data (Tag Assistant, HAR, logs, console)

**Rule:** NEVER use [CONFIG] to claim runtime behavior

### Forbidden Claims Without Evidence
Cannot claim these unless proven with evidence + mechanism:
- PASS / FIXED / BROKEN
- DUPLICATE / DOUBLE COUNTED
- DROPPED / MISSING
- "Tag is firing" (Tag Assistant visibility ≠ platform acceptance)

### Duplication Proof Rule
To claim duplication, MUST prove TWO sends for SAME business action with:
- event_name + timestamp window + transaction_id OR page_url
- If event_id exists, it's the primary correlation key

### user_id Dropped Proof Rule
To claim user_id is dropped, MUST show:
1. Inbound sGTM eventData contains user_id [RUNTIME]
2. Outbound vendor payload lacks user_id for same event [RUNTIME]
3. Mapping/config explains why [CONFIG]

## Common Failure Scenarios

### Scenario 1: Gate 3 FAILED - sGTM Tag Assistant Empty
**Symptom:** sGTM Tag Assistant has 0 messages

**Possible Causes:**
1. sGTM server not receiving requests from Worker
2. Cloudflare Worker not forwarding requests
3. DNS configuration incorrect (sgtm.domain.com)
4. Tag Assistant not connected to sGTM during test
5. sGTM preview mode not active

**Action Card Generated:**
- Location: Network/Infrastructure layer
- Verification Steps: Check Worker logs, Stape logs, DNS
- No GTM changes needed - infrastructure issue

### Scenario 2: Gate 2 FAILED - SOP Mismatch
**Symptom:** Data Tag request_path doesn't match sGTM client claim path

**Example:**
- Data Tag sends to: `/gtm-data`
- Data Client claims: `/data`
- Result: Events reach sGTM but no client claims them

**Action Card Generated:**
- Location: wGTM Data Tag OR sGTM Data Client
- Fix: Align both to use same path (e.g., `/data`)
- Validation: Re-export containers, re-run troubleshooter

### Scenario 3: Gate 4 Mutations Detected
**Symptom:** Field values differ between wGTM outbound and sGTM inbound

**Example:**
- wGTM: `transaction_id: "12345"`
- sGTM: `transaction_id: ""`
- Cause: Variable remapping drops value

**Action Card Generated:**
- Location: sGTM transformation/variable logic
- Fix: Review variable mappings in sGTM

## Extending the Tool

### Adding New Event Types
Edit `phase2_source_index()`:
```python
priority_events = [
    "view_item", "add_to_cart", "begin_checkout", "purchase",
    "view_item_list", "view_cart", "search",
    "your_custom_event"  # Add here
]
```

### Adding New Vendors
Edit `_inventory_gtm_container()`:
```python
# Add vendor detection logic
if "your_vendor" in tag_type.lower():
    for param in tag.get("parameter", []):
        if param.get("key") == "vendor_id":
            inventory["your_vendor_ids"].append({
                "id": param.get("value", ""),
                "container": container_type,
                "entity_type": "Tag",
                "entity_name": tag_name
            })
```

### Custom Root Cause Detection
Edit `_add_root_cause()` calls in phase methods to add domain-specific logic.

## Troubleshooting the Troubleshooter

### No Events Found in Source Index
**Cause:** Tag Assistant format not recognized or event name mismatch

**Fix:**
1. Check Tag Assistant export structure matches expected format
2. Verify event names in `priority_events` list match your events
3. Add debug print in `_index_tag_assistant()` to see raw structure

### Missing File Errors
**Cause:** Files don't match expected glob patterns

**Fix:**
1. Check filenames match patterns in `_find_file_pattern()`
2. Place files in correct directory (default: `original-data/`)
3. Use `--data-dir` flag to specify custom location

### Gate Always Shows UNKNOWN
**Cause:** Evidence extraction failing silently

**Fix:**
1. Check for exception messages in output (`⚠️ Error...`)
2. Add debug prints in relevant `_extract_*()` methods
3. Verify JSON structure matches expectations

## Best Practices

### 1. Capture Complete Evidence
- Export Tag Assistant recordings for BOTH web and server containers
- Enable sGTM preview mode during test
- Save worker code and Cloudflare settings
- Export GTM containers after any changes

### 2. Consistent Test Event
- Use the same test transaction for all evidence capture
- Note the transaction_id and event_id
- Capture at the same timestamp window

### 3. Iterative Troubleshooting
- Run troubleshooter to identify issue
- Fix ONE thing at a time
- Re-export evidence
- Re-run troubleshooter to verify fix
- Repeat until all gates pass

### 4. Documentation
- Save troubleshooter output after each run
- Document changes made between runs
- Keep history of Action Cards and resolutions

## Support and Contributing

### Reporting Issues
When reporting issues with the troubleshooter:
1. Include full output (use `--output` flag)
2. Sanitize any sensitive IDs/domains
3. Describe what you expected vs what you got
4. Include sample of problematic input file (sanitized)

### Feature Requests
Priority areas for enhancement:
- Additional vendor support (TikTok, Snapchat, etc.)
- HAR file parsing for true network proof
- Stape logs analysis integration
- Automatic fix application (where safe)
- HTML/PDF report generation

## License

This tool is provided as-is for troubleshooting GTM implementations. Modify as needed for your use case.

## Credits

Implements the evidence-first methodology specified in the GTM troubleshooting framework.
