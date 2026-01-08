Full Audit Report (evidence set: 2026-01-07 exports)

## Executive Summary
- SOP chain past /metrics is not observable because sGTM Tag Assistant contains no inbound events or tag logs and no /metrics network evidence was provided. (Evidence: `original-data/tag_assistant_sgtm_messerattach_com_2026_01_08.json`)
- user_id pipeline is broken: DataLayer uses top-level user_id, wGTM Variable/dlv - user_id reads user_data.user_id and resolves undefined, and sGTM Variable/EDV - user_id also expects user_data.user_id. (Evidence: `original-data/new begin checkout data layer.json`, `original-data/tag_assistant_messerattach_com_2026_01_08.json`, `original-data/GTM-MNRP4PF_workspace250.json`, `original-data/GTM-K3CQBMZ9_workspace39.json`)
- event_id is configured in the wGTM Tag/Data Tag payload but is not present in the DataLayer event model and cannot be verified end-to-end without /metrics or sGTM preview evidence. (Evidence: `original-data/GTM-MNRP4PF_workspace250.json`, `original-data/new view_iteam data layer.json`, `original-data/tag_assistant_sgtm_messerattach_com_2026_01_08.json`)
- Ecommerce payloads exist but with data-quality gaps: value/price/cart_total are strings, item_name contains unescaped quotes, user_data is empty, ecomm_pagetype is basket on cart/checkout samples, and item_brand coverage beyond samples is not determinable. (Evidence: `original-data/new cart view.json`, `original-data/new begin checkout data layer.json`, `original-data/new view_iteam data layer.json`, `original-data/tag_assistant_messerattach_com_2026_01_08.json`)
- Consent enforcement is not configured at the tag level in either layer (wGTM Tag/Data Tag consentStatus NOT_NEEDED; sGTM tags consentStatus NOT_SET). (Evidence: `original-data/GTM-MNRP4PF_workspace250.json`, `original-data/GTM-K3CQBMZ9_workspace39.json`)
- sGTM GA4 add_to_cart duplication risk exists because both sGTM Tag/GA4 Advanced and sGTM Tag/GA4 ADV add_to_cart are configured to fire on add_to_cart. (Evidence: `original-data/GTM-K3CQBMZ9_workspace39.json`)

## Current Situation Map
- Consent: Consent states are granted at ecommerce events in Tag Assistant. (Evidence: `original-data/tag_assistant_messerattach_com_2026_01_08.json`)
- DataLayer -> wGTM: view_item, add_to_cart, view_cart, begin_checkout include ecommerce.items and currency/value; user_id is top-level; user_data is empty; value/price are strings; ecomm_pagetype is basket for cart/checkout; provided sample shows begin_checkout only (no checkout event observed in this evidence). (Evidence: `original-data/new view_iteam data layer.json`, `original-data/new cart view.json`, `original-data/new begin checkout data layer.json`, `original-data/tag_assistant_messerattach_com_2026_01_08.json`)
- wGTM: wGTM Tag/Data Tag is configured to send to https://messerattach.com/metrics with request_path /data, add_consent_state true, and event_name_custom from Event page_view Override; Tag Assistant shows Data Tag firing on ecommerce events. (Evidence: `original-data/GTM-MNRP4PF_workspace250.json`, `original-data/tag_assistant_messerattach_com_2026_01_08.json`)
- Network/SOP: /metrics request method/status/caching are not observable. (Evidence: `original-data/tag_assistant_sgtm_messerattach_com_2026_01_08.json`)
- sGTM ingestion: Not determinable; sGTM Tag Assistant recording contains no inbound events. (Evidence: `original-data/tag_assistant_sgtm_messerattach_com_2026_01_08.json`)
- sGTM outbound: Not determinable; tags are configured but no preview evidence of firing. (Evidence: `original-data/GTM-K3CQBMZ9_workspace39.json`, `original-data/tag_assistant_sgtm_messerattach_com_2026_01_08.json`)
- Parallel sends: client-side tags fire on ecommerce events (LinkedIn Insight, FB - Page View, ms_uet_*, google_ads_calls, google_ads_800calls). (Evidence: `original-data/tag_assistant_messerattach_com_2026_01_08.json`)

## Inventory Table (IDs, templates, where used)
- wGTM container GTM-MNRP4PF exportTime 2026-01-07 17:54:43, containerVersionId 0. (Evidence: `original-data/GTM-MNRP4PF_workspace250.json`)
- sGTM container GTM-K3CQBMZ9 exportTime 2026-01-07 17:54:26, containerVersionId 0. (Evidence: `original-data/GTM-K3CQBMZ9_workspace39.json`)

ID / Key | Template | Where used
GT-NS9Z5FWG | wGTM Tag/Google Tag | server_container_url=https://messerattach.com/metrics; Tag Assistant shows gtm.init only (no ecommerce send_to evidence). (Evidence: `original-data/GTM-MNRP4PF_workspace250.json`, `original-data/tag_assistant_messerattach_com_2026_01_08.json`)
G-YCL5FGZNCV | GA4 Measurement ID | wGTM Variable/GA4 - ID; sGTM Tag/GA4 Advanced and sGTM Tag/GA4 ADV add_to_cart measurementId. (Evidence: `original-data/GTM-MNRP4PF_workspace250.json`, `original-data/GTM-K3CQBMZ9_workspace39.json`)
767740215 | Google Ads Conversion ID | wGTM Tag/google_ads_calls + google_ads_800calls; sGTM Tag/Google Ads Conversion Tracking + Remarketing. (Evidence: `original-data/GTM-MNRP4PF_workspace250.json`, `original-data/GTM-K3CQBMZ9_workspace39.json`)
srU-CMOM3OoYELeSi-4C, y0V4CNzM0uoYELeSi-4C, gM6CCLv40eoYELeSi-4C, oFJkCJX62uoYELeSi-4C | Google Ads labels | sGTM Tag/Google Ads Conversion Tracking labels (Checkout/Add_to_Cart/Purchase/Contact). (Evidence: `original-data/GTM-K3CQBMZ9_workspace39.json`)
ZLAFCNKDkusYELeSi-4C, WrSjCJnAiesYELeSi-4C | Google Ads call labels | wGTM Tag/google_ads_calls + google_ads_800calls labels. (Evidence: `original-data/GTM-MNRP4PF_workspace250.json`)
wGTM Tag/Data Tag endpoint | Stape Data Tag template | gtm_server_domain https://messerattach.com/metrics, request_path /data, event_name_custom {{Event page_view Override}}, add_consent_state true. (Evidence: `original-data/GTM-MNRP4PF_workspace250.json`)
sGTM Client/Data Client | Stape Data Client | acceptMultipleEvents true, generateClientId true; ingestion path not determinable from export alone. (Evidence: `original-data/GTM-K3CQBMZ9_workspace39.json`)
Event-name normalization | wGTM Variable/Event page_view Override | gtm.dom and gtm.historyChange -> page_view; gtm.scrollDepth -> scroll. (Evidence: `original-data/GTM-MNRP4PF_workspace250.json`)

## Event Chain Results Table
Join key:
- Primary: event_id (wGTM Variable/Unique Event ID resolves in Tag Assistant; not present in DataLayer event model). (Evidence: `original-data/tag_assistant_messerattach_com_2026_01_08.json`, `original-data/new view_iteam data layer.json`)
- Fallback: +/-3s + event_name + items_count/value/currency/page_url. (Evidence: `original-data/tag_assistant_messerattach_com_2026_01_08.json`)

Event | DataLayer payload | wGTM Tag/Data Tag fired | /metrics request | sGTM Client/Data Client claimed | sGTM Tag/GA4 Advanced fired | sGTM Ads tags fired
view_item | PASS (items/currency/value present; value string) | PASS | Not determinable | Not determinable | Not determinable | Not determinable
add_to_cart | PASS (items/currency/value present; value string) | PASS | Not determinable | Not determinable | Not determinable | Not determinable
begin_checkout | PASS (items/currency/value present; value string) | PASS | Not determinable | Not determinable | Not determinable | Not determinable
Evidence for PASS/Not determinable: `original-data/tag_assistant_messerattach_com_2026_01_08.json`, `original-data/tag_assistant_sgtm_messerattach_com_2026_01_08.json`, `original-data/new view_iteam data layer.json`, `original-data/new cart view.json`, `original-data/new begin checkout data layer.json`
Acceptance check: Not determinable from provided inputs (no GA4 DebugView/Realtime evidence). (Evidence: `original-data/tag_assistant_sgtm_messerattach_com_2026_01_08.json`)
Purchase: not observed in provided evidence. (Evidence: `original-data/tag_assistant_messerattach_com_2026_01_08.json`, `original-data/new begin checkout data layer.json`)

## Root Causes (by layer) + Exact Fixes
- DataLayer schema: value/price/cart_total are strings and item_name contains unescaped quotes; fix by emitting numeric values and escaping quotes before pushing to dataLayer. (Evidence: `original-data/new cart view.json`, `original-data/new begin checkout data layer.json`)
- DataLayer identity: user_id is top-level while wGTM Variable/dlv - user_id reads user_data.user_id; fix by aligning the key path (change DataLayer to user_data.user_id or change the variable to read user_id). (Evidence: `original-data/new begin checkout data layer.json`, `original-data/GTM-MNRP4PF_workspace250.json`, `original-data/tag_assistant_messerattach_com_2026_01_08.json`)
- DataLayer user_data: user_data is empty in ecommerce events; fix by pushing user_data only on validated blur/step completion and include an event key with the user_data update. (Evidence: `original-data/new begin checkout data layer.json`, `original-data/tag_assistant_messerattach_com_2026_01_08.json`)
- wGTM consent gating: wGTM Tag/Data Tag consentStatus is NOT_NEEDED; fix by applying consent requirements at tag level before forwarding. (Evidence: `original-data/GTM-MNRP4PF_workspace250.json`)
- sGTM consent gating: sGTM tags consentStatus are NOT_SET; fix by requiring consent at tag level server-side. (Evidence: `original-data/GTM-K3CQBMZ9_workspace39.json`)
- sGTM GA4 duplication risk: sGTM Tag/GA4 Advanced fires on t_ecomCore (includes add_to_cart) while sGTM Tag/GA4 ADV add_to_cart also fires on add_to_cart; fix by removing or scoping one tag. (Evidence: `original-data/GTM-K3CQBMZ9_workspace39.json`)
- sGTM GA4 add_to_cart overrides: sGTM Tag/GA4 ADV add_to_cart has addParam false for event_id/items/value, which can drop ecommerce parameters; fix by setting addParam true or removing the tag if GA4 Advanced is authoritative. (Evidence: `original-data/GTM-K3CQBMZ9_workspace39.json`)
- SOP observability gap: no /metrics network evidence and no sGTM preview logs; fix by capturing a synchronized wGTM + sGTM preview and /metrics requests. (Evidence: `original-data/tag_assistant_sgtm_messerattach_com_2026_01_08.json`)
- UET pagetype mismatch: ecomm_pagetype is basket on cart/checkout samples; fix by mapping basket -> cart (or update DataLayer). (Evidence: `original-data/new cart view.json`, `original-data/new begin checkout data layer.json`)

## Routing Classification + Duplication Controls
- gtag classification: Not determinable from provided inputs (Google Tag exists; no network evidence of routing). (Evidence: `original-data/GTM-MNRP4PF_workspace250.json`, `original-data/tag_assistant_messerattach_com_2026_01_08.json`)
- Configured send paths:
  - wGTM Tag/Data Tag -> https://messerattach.com/metrics/data (fires on ecommerce events). (Evidence: `original-data/GTM-MNRP4PF_workspace250.json`, `original-data/tag_assistant_messerattach_com_2026_01_08.json`)
  - sGTM Tag/GA4 Advanced and sGTM Tag/Google Ads Conversion Tracking configured, but not observed firing. (Evidence: `original-data/GTM-K3CQBMZ9_workspace39.json`, `original-data/tag_assistant_sgtm_messerattach_com_2026_01_08.json`)
  - wGTM Tag/Google Tag GT-NS9Z5FWG configured with server_container_url /metrics; Tag Assistant shows gtm.init only. (Evidence: `original-data/GTM-MNRP4PF_workspace250.json`, `original-data/tag_assistant_messerattach_com_2026_01_08.json`)
  - Client-side call conversions (google_ads_calls, google_ads_800calls) fire in wGTM. (Evidence: `original-data/tag_assistant_messerattach_com_2026_01_08.json`)
- Routing classification per destination:
  - GA4 ecommerce: Not determinable from provided inputs (server tags configured but not observed; no network evidence). (Evidence: `original-data/GTM-K3CQBMZ9_workspace39.json`, `original-data/tag_assistant_sgtm_messerattach_com_2026_01_08.json`)
  - Google Ads conversions: Not determinable from provided inputs for server-side; client-side call conversions are observed. (Evidence: `original-data/tag_assistant_messerattach_com_2026_01_08.json`, `original-data/GTM-K3CQBMZ9_workspace39.json`)
  - Remarketing: Not determinable from provided inputs. (Evidence: `original-data/GTM-K3CQBMZ9_workspace39.json`, `original-data/tag_assistant_sgtm_messerattach_com_2026_01_08.json`)
- Keep / Disable / Move server-side (policy):
  - Keep: wGTM Tag/Data Tag as the SOP sender once sGTM ingestion is confirmed. (Evidence: `original-data/GTM-MNRP4PF_workspace250.json`)
  - Keep client-side: wGTM Tag/google_ads_calls + google_ads_800calls for call tracking. (Evidence: `original-data/tag_assistant_messerattach_com_2026_01_08.json`)
  - Move/justify: wGTM Tag/ms_uet_view_item, ms_uet_add_to_cart, ms_uet_checkout, ms_uet_purchase should be moved server-side or explicitly documented as exceptions. (Evidence: `original-data/tag_assistant_messerattach_com_2026_01_08.json`)
- Deduplication rule: event_id must be consistent across any hybrid path; current event_id presence is not verifiable end-to-end. (Evidence: `original-data/GTM-MNRP4PF_workspace250.json`, `original-data/tag_assistant_messerattach_com_2026_01_08.json`, `original-data/tag_assistant_sgtm_messerattach_com_2026_01_08.json`)

## Consent + PII Findings
- Consent states are granted at ecommerce events in wGTM Tag Assistant. (Evidence: `original-data/tag_assistant_messerattach_com_2026_01_08.json`)
- wGTM Tag/Data Tag consentStatus is NOT_NEEDED and sGTM tags consentStatus are NOT_SET. (Evidence: `original-data/GTM-MNRP4PF_workspace250.json`, `original-data/GTM-K3CQBMZ9_workspace39.json`)
- DataLayer user_data is empty and customer variables resolve undefined at begin_checkout. (Evidence: `original-data/new begin checkout data layer.json`, `original-data/tag_assistant_messerattach_com_2026_01_08.json`)
- No PII is present in the observed ecommerce payloads; if user_data is required, it must be pushed explicitly and consent gated. (Evidence: `original-data/tag_assistant_messerattach_com_2026_01_08.json`, `original-data/new begin checkout data layer.json`)

## SOP Findings + Hardening Actions
- Ingestion claim: Not determinable; sGTM Tag Assistant recording contains no inbound events or tags. (Evidence: `original-data/tag_assistant_sgtm_messerattach_com_2026_01_08.json`)
- Caching/WAF/Bot interference: Not determinable from provided inputs; no cache/WAF evidence supplied. (Evidence: `original-data/tag_assistant_sgtm_messerattach_com_2026_01_08.json`)
- Request integrity: Not determinable; no /metrics network capture provided. (Evidence: `original-data/tag_assistant_sgtm_messerattach_com_2026_01_08.json`)
- Hardening actions (required to implement/verify):
  - Cloudflare: bypass cache for /metrics/* and exempt from WAF/Bot challenges and redirects. (Evidence gap: no Cloudflare rules provided)
  - WP Rocket: exclude /metrics/* from caching/optimization. (Evidence gap: no WP Rocket rules provided)
  - Worker: preserve method/content-type/body and forward to the exact client-claimed ingestion path. (Evidence gap: no /metrics network or sGTM client-claim evidence)
  - Monitoring: add logging for /metrics non-2xx and latency. (Evidence gap: no logs provided)

## Prioritized Action Plan (Critical/High/Medium/Low; Effort; Exact changes; Validation)
- Critical | Effort: M | Change: Capture synchronized wGTM + sGTM preview and /metrics network requests for view_item, add_to_cart, begin_checkout. | Validation: sGTM preview shows sGTM Client/Data Client claim and GA4 tag firing; /metrics requests are 2xx and not cached. (Evidence: `original-data/tag_assistant_sgtm_messerattach_com_2026_01_08.json`)
- Critical | Effort: S | Change: Align user_id mapping (change DataLayer to user_data.user_id or change wGTM Variable/dlv - user_id to read user_id; update sGTM Variable/EDV - user_id to match). | Validation: Tag Assistant shows user_id resolved; sGTM eventData includes user_id. (Evidence: `original-data/new begin checkout data layer.json`, `original-data/GTM-MNRP4PF_workspace250.json`, `original-data/GTM-K3CQBMZ9_workspace39.json`, `original-data/tag_assistant_messerattach_com_2026_01_08.json`)
- High | Effort: M | Change: Normalize value/price/cart_total to numbers and escape quotes in item_name; enforce item_brand fallback where missing. | Validation: DataLayer samples and Tag Assistant payloads show numeric values and clean item_name. (Evidence: `original-data/new cart view.json`, `original-data/new begin checkout data layer.json`, `original-data/tag_assistant_messerattach_com_2026_01_08.json`)
- High | Effort: S | Change: Apply consent requirements to wGTM Tag/Data Tag and sGTM tags. | Validation: tags do not fire when consent denied. (Evidence: `original-data/GTM-MNRP4PF_workspace250.json`, `original-data/GTM-K3CQBMZ9_workspace39.json`)
- Medium | Effort: S | Change: Remove or scope sGTM Tag/GA4 ADV add_to_cart (or set addParam true for event_id/items/value) to avoid duplication and parameter loss. | Validation: only one GA4 server tag fires for add_to_cart and ecommerce params are preserved. (Evidence: `original-data/GTM-K3CQBMZ9_workspace39.json`)
- Medium | Effort: S | Change: Map ecomm_pagetype basket -> cart for UET (or update DataLayer). | Validation: Tag Assistant shows ecomm_pagetype cart on cart/checkout. (Evidence: `original-data/new cart view.json`, `original-data/new begin checkout data layer.json`, `original-data/tag_assistant_messerattach_com_2026_01_08.json`)
- Low | Effort: S | Change: Add /metrics error and latency logging. | Validation: logs/metrics available for non-2xx and latency. (Evidence gap: no logs provided)
