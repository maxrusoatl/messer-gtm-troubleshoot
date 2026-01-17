# GTM Troubleshooter - Quick Start

## What This Tool Does

Audits your GTM tracking pipeline (WooCommerce → wGTM → Cloudflare Worker → sGTM) and identifies exactly where tracking breaks down, with evidence-backed findings and actionable fixes.

## 5-Minute Setup

### 1. Prepare Your Data

Create a folder called `original-data/` and put these files in it:

**Required:**
- Your web GTM export (e.g., `GTM-XXXXX_workspace.json`)
- Your server GTM export (e.g., `GTM-YYYYY_workspace.json`)
- Tag Assistant web recording (export from Chrome extension)
- Tag Assistant server recording (export from sGTM preview mode)

**Optional but helpful:**
- Your Cloudflare Worker code (`worker.js`)
- Sample datalayer files (e.g., `purchase_datalayer.json`)

### 2. Run the Tool

```bash
python3 gtm_troubleshooter.py
```

That's it! The output shows exactly where your tracking fails.

## Understanding the Output

### The 5 Gates

Your tracking goes through 5 gates. Each must pass for tracking to work:

1. **Gate 1: Browser Network** - Does the browser actually send the request?
   - ✓ PASS = Good
   - ❌ FAIL = Browser isn't sending (check if tags fire)

2. **Gate 2: SOP Contract** - Do the paths match up?
   - ✓ PASS = Worker and GTM agree on paths
   - ❌ FAIL = Path mismatch - events reach sGTM but no client claims them

3. **Gate 3: sGTM Inbound** - Does sGTM receive the event?
   - ✓ PASS = sGTM got the event
   - ❌ FAIL = sGTM didn't receive it (infrastructure issue)

4. **Gate 4: Data Integrity** - Do the values match across layers?
   - ✓ PASS = No data loss
   - ❌ FAIL = Fields are being dropped or changed

5. **Gate 5: Identity & Dedup** - Is deduplication working?
   - ✓ PASS = event_id present, dedup configured
   - ❌ FAIL = Missing event_id or dedup logic

### Symbols

- ✓ = VERIFIED (passed with evidence)
- ❌ = FAILED (proven to fail)
- ⚠️ = UNKNOWN (need more evidence)
- ⏸️ = BLOCKED (can't test because upstream failed)

## Example Output

```
Gate Results Summary:
  ✓ gate1: VERIFIED      ← Browser sends requests
  ✓ gate2: VERIFIED      ← Paths match
  ❌ gate3: FAILED        ← sGTM NOT receiving! ⚠️
  ⏸️ gate4: BLOCKED      ← Can't test until Gate 3 passes
  ⏸️ gate5: BLOCKED      ← Can't test until Gate 3 passes

Root Causes: 1
ACTION CARD #1
  Problem: sGTM Tag Assistant has zero messages
  Fix: Check Cloudflare Worker logs and Stape server status
```

## Common Issues & Quick Fixes

### Issue 1: "Gate 3 FAILED - sGTM Tag Assistant is empty"

**What it means:** Events aren't reaching your sGTM server

**Quick checks:**
1. Go to Cloudflare → Workers → Check if route is active
2. Check Stape dashboard - is container running?
3. DNS: Does `sgtm.yourdomain.com` point to Stape?
4. Try accessing `https://sgtm.yourdomain.com/healthz` - should return 200 OK

**Most common cause:** Forgot to activate sGTM preview mode when capturing Tag Assistant data

### Issue 2: "Gate 2 FAILED - SOP Mismatch"

**What it means:** Your Data Tag and sGTM client are using different paths

**Quick fix:**
1. Open wGTM → Tags → Data Tag
2. Note the "Request Path" (e.g., `/data`)
3. Open sGTM → Clients → Data Client
4. Verify it claims the same path
5. If different, make them match and republish both containers

### Issue 3: "Gate 1 FAILED - No Golden Test event"

**What it means:** No ecommerce events found in your data

**Quick fix:**
1. Make sure you exported Tag Assistant DURING a test purchase
2. Check that Tag Assistant recorded the full journey (cart → checkout → purchase)
3. Re-run test and re-export Tag Assistant

## Next Steps After First Run

1. **Fix the highest gate that failed** - Start from Gate 1
2. **Capture new evidence** - Re-export Tag Assistant after fix
3. **Re-run the tool** - Verify the gate now passes
4. **Repeat** - Move to next gate

## Getting Help

If output shows:
- **"UNKNOWN"** - You need more data files (check "Missing Evidence" section at end)
- **"BLOCKED"** - Fix the upstream gate first
- **"Root Causes: 0"** - All gates passed! Your tracking is working.

## Pro Tips

- Always enable sGTM **Preview Mode** before testing
- Do a fresh test purchase for each troubleshooting session
- Save each report with date: `python3 gtm_troubleshooter.py --output report_2024-01-15.txt`
- Fix ONE gate at a time, then re-run

## File Naming Guide

The tool auto-detects files. If it can't find yours, rename them:

- Web GTM: Should have "workspace" and be marked usageContext: "WEB"
- Server GTM: Should have "workspace" and be marked usageContext: "SERVER"  
- Tag Assistant Web: Should have "tag_assistant" (NOT "sgtm")
- Tag Assistant Server: Should have "tag_assistant_sgtm"

## That's It!

Run `python3 gtm_troubleshooter.py` and follow the action cards. Each one tells you EXACTLY what to change and where.

Questions? See `GTM_TROUBLESHOOTER_README.md` for detailed documentation.
