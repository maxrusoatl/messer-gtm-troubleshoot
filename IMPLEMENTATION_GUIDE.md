# Messer GTM Implementation Guide
## Complete Strategy with Clear Distinctions

**Version: 2.0 - UPDATED** (Previous version incorrectly stated only 1 fix needed)

---

## Quick Reference: What is What?

| Term | Full Name | Purpose | Container ID |
|------|-----------|---------|--------------|
| **wGTM** | Web Google Tag Manager | Runs in browser, collects events | GTM-MNRP4PF |
| **sGTM** | Server-side GTM | Runs on server (Stape), forwards to platforms | GTM-K3CQBMZ9 |
| **gtag** | Google Tag | Google's tracking code (part of wGTM) | GT-NS9Z5FWG |
| **Stape.io** | Hosting Provider | Hosts the sGTM container | sgtm.messerattach.com |
| **Data Tag** | Stape Data Tag | wGTM tag that sends events to sGTM | Tag ID #310 |

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                   BROWSER                                        │
│                                                                                  │
│  ┌────────────┐     ┌──────────────┐     ┌─────────────────────────────────────┐│
│  │WooCommerce │────►│  DataLayer   │────►│              wGTM                    ││
│  │ + Complianz│     │              │     │          GTM-MNRP4PF                 ││
│  └────────────┘     └──────────────┘     │                                     ││
│                                          │  ┌─────────────────────────────────┐││
│                                          │  │      DATA TAG #310              │││
│                                          │  │   FIX #1: Trigger 96 → 313      │││
│                                          │  │   FIX #2: event_id variable     │││
│                                          │  │   → /metrics/data               │││
│                                          │  └──────────────┬──────────────────┘││
│                                          │                 │                    ││
│                                          │  ┌─────────────────────────────────┐││
│                                          │  │     GTAG GT-NS9Z5FWG            │││
│                                          │  │   → /metrics (working)          │││
│                                          │  └──────────────┬──────────────────┘││
│                                          │                 │                    ││
│                                          │  ┌─────────────────────────────────┐││
│                                          │  │   CLIENT-SIDE TAGS              │││
│                                          │  │   • MS UET (no sGTM path)       │││
│                                          │  │   • LinkedIn Insight            │││
│                                          │  │   • FB Pixel (uses {{Event Id}})│││
│                                          │  └──────────────┬──────────────────┘││
│                                          └─────────────────┼────────────────────┘│
└────────────────────────────────────────────────────────────┼─────────────────────┘
                                                             │
                               ┌─────────────────────────────┼─────────────────────┐
                               │                             ▼                     │
                               │  ┌──────────────────────────────────────────────┐ │
                               │  │              CF WORKER PROXY                 │ │
                               │  │         messerattach.com/metrics/*           │ │
                               │  │                                              │ │
                               │  │  Routes:                                     │ │
                               │  │    /metrics/* → sgtm.messerattach.com        │ │
                               │  │    /metrics/data → Data Client               │ │
                               │  │    /metrics/g/collect → GA4 Client           │ │
                               │  └──────────────────────────────────────────────┘ │
                               │                             │                     │
                               │                      STAPE.IO                     │
                               │                             ▼                     │
                               │  ┌──────────────────────────────────────────────┐ │
                               │  │              sGTM CONTAINER                  │ │
                               │  │            GTM-K3CQBMZ9                       │ │
                               │  │                                              │ │
                               │  │  CLIENTS:                                    │ │
                               │  │    • Data Client (#18) → claims /data        │ │
                               │  │    • GTM Web Container (#69) → gtag events   │ │
                               │  │                                              │ │
                               │  │  TAGS:                                       │ │
                               │  │    • GA4 Advanced (FIX #3: add triggers!)    │ │
                               │  │    • Google Ads (Checkout, ATC, Purchase)    │ │
                               │  │    • FB CAPI (ViewContent, ATC, Checkout,    │ │
                               │  │              Purchase)                       │ │
                               │  └──────────────────────────────────────────────┘ │
                               └───────────────────────────────────────────────────┘
                                                             │
                                                             ▼
                               ┌─────────────────────────────────────────────────────┐
                               │                  PLATFORMS                          │
                               │                                                     │
                               │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐│
                               │  │   GA4   │  │ G Ads   │  │  Meta   │  │LinkedIn ││
                               │  │(Server) │  │(Server) │  │ (CAPI)  │  │ (CAPI)  ││
                               │  └─────────┘  └─────────┘  └─────────┘  └─────────┘│
                               └─────────────────────────────────────────────────────┘
```

---

## THREE Fixes Required

### Fix #1: wGTM Data Tag Trigger (CRITICAL)

**Problem:** Data Tag #310 uses trigger `ce_purchase` (ID 96) which ONLY fires on purchase events.

**Solution:** Change trigger from #96 to #313 (`Trigger - Ecom Core Events`).

**Steps:**
1. Open GTM → Container GTM-MNRP4PF
2. Tags → "Data Tag" (ID 310)
3. Click Triggering section
4. Remove `ce_purchase`
5. Add `Trigger - Ecom Core Events` (ID 313)
6. Save (DO NOT PUBLISH YET - complete Fix #2 first)

**What Trigger #313 Fires On:**
```
page_view, view_cart, add_payment_info, add_to_cart, begin_checkout,
find_location, generate_lead, login, purchase, refund, search,
share, sign_up, view_item, view_item_list, view_search_results
```

---

### Fix #2: wGTM Event ID Mismatch (CRITICAL)

**Problem:** Facebook deduplication is broken because FB Pixel and Data Tag use DIFFERENT event ID variables.

| Tag | Variable Used | Template Source |
|-----|---------------|-----------------|
| FB Pixel (Tag 112) | `{{Event Id}}` | mbaersch template |
| Data Tag (Tag 310) | `{{Unique Event ID}}` | stape-io template |

**Result:** Facebook sees browser and server events as TWO DIFFERENT events → double counting, poor Event Match Quality.

**Solution:** Change Data Tag to use the SAME variable as FB Pixel.

**Steps:**
1. In GTM-MNRP4PF, go to Tags → "Data Tag" (ID 310)
2. Find the `event_id` parameter in the tag configuration
3. Change from `{{Unique Event ID}}` to `{{Event Id}}`
4. Save
5. Submit and Publish wGTM container
6. Proceed to Fix #3 in sGTM

---

### Fix #3: sGTM GA4 Advanced Triggers (CRITICAL)

**Problem:** GA4 Advanced tag (ID 16) only fires on `purchase` trigger, ignoring all other ecommerce events.

| Current | Missing |
|---------|---------|
| Trigger 54 (purchase) | Trigger 12 (t_engagement) |
| | Trigger 14 (t_ecomCore) |

**Result:** Even after fixing wGTM, sGTM will only forward purchase events to GA4. All other events are discarded.

**Solution:** Add missing triggers to GA4 Advanced tag.

**Steps:**
1. Open GTM → Container GTM-K3CQBMZ9 (Server Container)
2. Tags → "GA4 Advanced" (ID 16)
3. Click Triggering section
4. Keep `purchase` trigger (ID 54)
5. ADD `t_engagement` trigger (ID 12)
6. ADD `t_ecomCore` trigger (ID 14)
7. Save → Submit → Publish sGTM container

**Trigger Details:**
| Trigger | ID | Events |
|---------|-----|--------|
| t_engagement | 12 | page_view, view_item, scroll, video events |
| t_ecomCore | 14 | add_to_cart, begin_checkout, view_cart, add_payment_info |
| purchase | 54 | purchase (already attached) |

---

## Platform-by-Platform Strategy

### 1. Google Analytics 4 (GA4)

| Path | Status | Notes |
|------|--------|-------|
| wGTM → gtag → /metrics → sGTM GA4 Client | ✅ Working | 524 messages observed |
| wGTM → Data Tag → /metrics/data → sGTM GA4 Tag | ❌ Broken | Needs Fix #1, #2, #3 |

**After All Fixes:** Both paths will work. The gtag path handles basic pageviews; the Data Tag path handles enhanced ecommerce.

### 2. Google Ads

| Path | Status | Tags |
|------|--------|------|
| wGTM → Data Tag → sGTM | ❌ Broken | Checkout, Add to Cart, Purchase |
| wGTM → Client-side | ✅ Working | google_ads_calls, google_ads_800calls |

**Strategy:**
- Server-side for conversion tracking (after fixes)
- Client-side for call tracking (must stay client-side)

**Enhanced Conversions:** Already configured in sGTM tags using:
- `{{EDV - User Data - Billing - Email}}`
- `{{EDV - User Data - Billing - Phone}}`
- `{{EDV - User Data - Billing - First Name}}`
- etc.

### 3. Meta (Facebook)

| Path | Status | Tags |
|------|--------|------|
| wGTM → Data Tag → sGTM CAPI | ❌ Broken | ViewContent, AddToCart, Checkout, Purchase |
| wGTM → FB Pixel (client-side) | ✅ Working | FB - Page View |

**Deduplication Strategy (CURRENTLY BROKEN):**
- FB Pixel uses `{{Event Id}}` (mbaersch template)
- Data Tag currently uses `{{Unique Event ID}}` (stape-io template)
- **These are DIFFERENT variables → double counting!**

**After Fix #2:**
- Both paths will use `{{Event Id}}`
- Meta will properly deduplicate browser + server events
- Event Match Quality score will improve

### 4. Microsoft Ads (UET)

| Path | Status | Notes |
|------|--------|-------|
| wGTM → Client-side UET | ✅ Working | **NO SGTM PATH AVAILABLE** |

**Why No Server-Side:**
Microsoft does not offer a Conversions API (CAPI) like Meta or Google. UET must run client-side.

**Current Tags (all working):**
- `ms_uet_base` - Base tracking
- `ms_uet_view_item` - Product views
- `ms_uet_add_to_cart` - Add to cart
- `ms_uet_checkout` - Checkout
- `ms_uet_purchase` - Purchase

**Strategy:** Keep as-is. No changes needed.

### 5. LinkedIn

| Path | Status | Notes |
|------|--------|-------|
| wGTM → LinkedIn Insight | ✅ Working | Client-side pixel |
| sGTM → LinkedIn CAPI | ⚠️ Available | Not configured but possible |

**Strategy:**
- Current: Client-side Insight tag (working)
- Optional: Add LinkedIn CAPI in sGTM for better attribution

---

## Naming Conventions (Existing)

### wGTM Variables
| Pattern | Example | Usage |
|---------|---------|-------|
| `dlv_xxx` | `dlv_value`, `dlv_transactionID` | DataLayer Variables |
| `cjs - xxx` | `cjs - Items with Index` | Custom JavaScript |
| `Customers xxx` | `Customers Email`, `Customers Phone Number` | User data |
| Direct | `Event Id`, `External ID`, `Facebook Pixel` | Single-purpose |

### sGTM Variables
| Pattern | Example | Usage |
|---------|---------|-------|
| `EDV_xxx` | `EDV_ecommerce.value`, `EDV_ecommerce.items` | Event Data Variables |
| `EDV - xxx` | `EDV - client_id`, `EDV - user_id` | Event Data (alternate) |
| `Constant - xxx` | `Constant - FB CAPI Access Token` | Constants |

### Triggers
| Container | Pattern | Example |
|-----------|---------|---------|
| wGTM | `ce_xxx` | `ce_purchase`, `ce_view_item`, `ce_add_to_cart` |
| wGTM | `Trigger - xxx` | `Trigger - Ecom Core Events` |
| sGTM | `t_xxx` | `t_ecomCore`, `t_engagement` |
| sGTM | Event name | `purchase`, `begin_checkout`, `add_to_cart` |

---

## What's Already Configured Correctly

### wGTM Data Tag #310 (Partial - needs 2 fixes)
```
✅ gtm_server_domain: https://messerattach.com/metrics
✅ request_path:      /data
   (Template combines: domain + path → /metrics/data)
✅ add_data_layer:  true (sends full dataLayer)
✅ add_consent:     true (sends consent state)
✅ add_cookie:      true (sends common cookies)
❌ event_id:        {{Unique Event ID}} → CHANGE TO {{Event Id}}
✅ transaction_id:  {{dlv_transactionID}}
✅ value:           {{dlv_value}}
✅ currency:        {{dlv_ecommerce_currency}}
✅ items:           {{cjs - Items with Index}}
✅ user_data:       email, phone, name (SHA256 hashed)
```

### sGTM Data Client #18
```
✅ Path:            /data
✅ Priority:        102
✅ Status:          Ready to receive
```

### sGTM Tags (Partial - GA4 needs fix)
```
❌ GA4 Advanced:                     Only purchase trigger (NEEDS FIX #3)
✅ Google Ads - Checkout:            begin_checkout
✅ Google Ads - Add to Cart:         add_to_cart
✅ Google Ads - Purchase:            purchase
✅ FB CAPI - ViewContent:            view_item
✅ FB CAPI - AddToCart:              add_to_cart
✅ FB CAPI - Begin Checkout:         begin_checkout
✅ FB CAPI - Purchase:               purchase
```

---

## Event Flow After All Fixes

### 1. User Views Product
```
DataLayer: view_item
    ↓
wGTM: Data Tag fires (trigger #313 matches view_item)
      event_id = {{Event Id}} (same as FB Pixel)
    ↓
POST /metrics/data → CF Worker → sGTM
    ↓
sGTM Data Client receives event
    ↓
Tags fire (with triggers 12, 14, 54):
  • GA4 Advanced → GA4 (t_engagement trigger)
  • FB CAPI - ViewContent → Meta (with matching event_id for dedup)
```

### 2. User Adds to Cart
```
DataLayer: add_to_cart
    ↓
wGTM: Data Tag fires + ms_uet_add_to_cart fires
    ↓
Data Tag → sGTM → GA4 (t_ecomCore), Google Ads, FB CAPI
ms_uet → Microsoft UET (direct, no server path available)
```

### 3. User Purchases
```
DataLayer: purchase
    ↓
wGTM: Data Tag fires + ms_uet_purchase fires
    ↓
Data Tag → sGTM:
  • GA4 Advanced (purchase trigger)
  • Google Ads Purchase (with Enhanced Conversions)
  • FB CAPI Purchase (with event_id for dedup)

ms_uet_purchase → Microsoft UET (direct)
```

---

## Event ID (Deduplication) - CORRECTED

### The Problem (Current State)
```
FB Pixel (Tag 112): uses {{Event Id}} (mbaersch template)
    ↓
Generates: "1703789245123_a7b3c9d"
    ↓
Sent to Meta browser-side

Data Tag (Tag 310): uses {{Unique Event ID}} (stape-io template)
    ↓
Generates: DIFFERENT value like "1703789245456_x8y9z0"
    ↓
Sent to sGTM → FB CAPI → Meta server-side

Result: Meta sees TWO different events → double counting!
```

### The Fix (After Fix #2)
```
FB Pixel (Tag 112): uses {{Event Id}}
Data Tag (Tag 310): uses {{Event Id}} (CHANGED from Unique Event ID)
    ↓
SAME event_id value sent to both browser and server
    ↓
Meta sees matching event_ids → deduplicates → counts once
```

---

## What NOT to Do

### ❌ Don't Create New Variables
The existing variables work. Creating duplicates causes confusion.

### ❌ Don't Create New Data Tags
The existing Data Tag is properly configured (except for the 2 fixes needed).

### ❌ Don't Skip the sGTM Fix
Even if wGTM sends all events, sGTM GA4 will ignore them without Fix #3.

### ❌ Don't Remove Client-Side Tags
MS UET must stay client-side (no CAPI option).
FB Pixel stays for deduplication with CAPI.

---

## Implementation Order

| Step | Container | Action | Publish? |
|------|-----------|--------|----------|
| 1 | wGTM | Update Data Tag trigger (96 → 313) | No |
| 2 | wGTM | Change event_id to {{Event Id}} | Yes |
| 3 | sGTM | Add triggers 12, 14 to GA4 Advanced | Yes |

---

## Verification Checklist

### After Publishing wGTM Fixes

1. **wGTM Tag Assistant:**
   - [ ] Data Tag shows as "Fired" on view_item
   - [ ] Data Tag shows as "Fired" on add_to_cart
   - [ ] Data Tag shows as "Fired" on begin_checkout
   - [ ] Data Tag event_id matches FB Pixel event_id (SAME VALUE)

2. **Network Tab:**
   - [ ] POST to /metrics/data for each event
   - [ ] Payload includes event_id parameter

### After Publishing sGTM Fix

3. **sGTM Tag Assistant:**
   - [ ] Messages count > 0
   - [ ] Events include: view_item, add_to_cart, begin_checkout
   - [ ] **GA4 Advanced tag firing on ALL events (not just purchase)**
   - [ ] FB CAPI tags firing

4. **GA4 Real-Time:**
   - [ ] view_item events appearing
   - [ ] add_to_cart events appearing
   - [ ] Ecommerce data populated

5. **Meta Events Manager:**
   - [ ] Server events appearing
   - [ ] Deduplication working (no duplicates)
   - [ ] Event Match Quality score improving

6. **Stape Logs:**
   - [ ] /metrics/data requests appearing
   - [ ] 200 OK responses
   - [ ] Full payload in requests

---

## Summary

| Action | Container | What | Status |
|--------|-----------|------|--------|
| **FIX #1** | wGTM | Data Tag trigger: 96 → 313 | **Required** |
| **FIX #2** | wGTM | Data Tag event_id: {{Unique Event ID}} → {{Event Id}} | **Required** |
| **FIX #3** | sGTM | GA4 Advanced triggers: add 12 + 14 | **Required** |
| Keep | wGTM | All other variables | Working |
| Keep | wGTM | MS UET tags | Working (no sGTM option) |
| Keep | wGTM | FB Pixel | Working (for dedup) |
| Keep | sGTM | Other tags | Ready |
| Keep | sGTM | All clients | Ready |
| Verify | sGTM | Conversion Linker (Tag 46) | Check trigger covers Data Client |

**Three fixes required across both containers.**

---

*Document Version: 2.0*
*Created: December 28, 2024*
*Updated: December 28, 2024 - Added Fix #2 (event_id) and Fix #3 (sGTM GA4 triggers)*
