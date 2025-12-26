Executive Summary

GA4 e-commerce events are not reaching GA4 because the Data Tag fires only on purchase, sGTM GA4 tags cover only add_to_cart/purchase, and GA4 client is missing while Google Tag proxies to /metrics/g/collect. Source: wGTM export GTM-MNRP4PF_workspace247.json, sGTM export GTM-K3CQBMZ9_workspace36.json, Tag Assistant chunked_output/tag_assistant_messerattach_com_2025_12_24_messages_chunk_24.json.
User-ID is not captured end-to-end because dataLayer uses top-level user_id, variables read user_data.user_id, the value is hashed, and GA4 Advanced stores it as a user property instead of user_id. Source: messer datalayers new.txt, Tag Assistant chunked_output/tag_assistant_messerattach_com_2025_12_24_messages_chunk_24.json, wGTM export GTM-MNRP4PF_workspace247.json, sGTM export GTM-K3CQBMZ9_workspace36.json.
Data layer shows valid GA4-style ecommerce objects for view_item/add_to_cart/begin_checkout, so the issue is routing rather than data layer content. Source: Tag Assistant chunked_output/tag_assistant_messerattach_com_2025_12_24_messages_chunk_24.json, messer datalayers new.txt.
PII hygiene risk exists because add_data_layer is enabled while dataLayer pushes raw email/phone, and user_data mapping does not match the pushed keys. Source: wGTM export GTM-MNRP4PF_workspace247.json, messer datalayers new.txt.
Consent Mode v2 signals are present client-side, but server tags are not explicitly gated and ads_data_redaction shows false. Source: Tag Assistant chunked_output/tag_assistant_messerattach_com_2025_12_24_messages_chunk_24.json, sGTM export GTM-K3CQBMZ9_workspace36.json.
sGTM hit logs are missing/empty, so server-side hit processing cannot be verified; this is a core troubleshooting blocker. Source: stape io logs messer.csv, tag_assistant_sgtm_messerattach_com_2025_12_24.json.

Critical Troubleshooting

sGTM hit logs are missing/empty, so server-side hit processing cannot be verified; this is a core troubleshooting blocker. Source: stape io logs messer.csv, tag_assistant_sgtm_messerattach_com_2025_12_24.json.
GA4 e-commerce absence root cause: Data Tag only fires on ce_purchase, sGTM GA4 coverage is limited, and GA4 client is removed while gtag hits go to /metrics/g/collect. Source: wGTM export GTM-MNRP4PF_workspace247.json, sGTM export GTM-K3CQBMZ9_workspace36.json, Tag Assistant chunked_output/tag_assistant_messerattach_com_2025_12_24_messages_chunk_24.json.
GA4 e-commerce fix summary: fire Data Tag on all ecommerce/pageview events and add GA4 Advanced tags for missing events, or re-enable GA4 Client if keeping gtag proxying. Source: wGTM export GTM-MNRP4PF_workspace247.json, sGTM export GTM-K3CQBMZ9_workspace36.json.
User-ID failure root cause: dataLayer top-level user_id is not mapped, and GA4 Advanced uses user properties + hashing. Source: messer datalayers new.txt, Tag Assistant chunked_output/tag_assistant_messerattach_com_2025_12_24_messages_chunk_24.json, wGTM/sGTM exports.
User-ID fix summary: map top-level user_id into eventData without hashing and set GA4 user_id parameter (not user property). Source: wGTM export GTM-MNRP4PF_workspace247.json, sGTM export GTM-K3CQBMZ9_workspace36.json.

Part 1: Client-Side Foundation - Data Tag & wGTM

Data Tag is configured with add_data_layer, add_common, add_common_cookie, add_consent_state, and request_path: /data, but it fires only on ce_purchase. Source: wGTM export GTM-MNRP4PF_workspace247.json.
Event name override maps gtm.dom/gtm.historyChange to page_view and gtm.scrollDepth to scroll, which is correct but currently unused due to the trigger. Source: wGTM export GTM-MNRP4PF_workspace247.json.
add_data_layer: true means raw user_data can be sent server-side; data layer samples show raw email/phone during checkout. Source: wGTM export GTM-MNRP4PF_workspace247.json, messer datalayers new.txt.
Data Tag custom_data includes transaction_id/value/currency/items/event_id/fbp/fbc/search_term but omits coupon_code, item_list_name, and msclkid. Source: wGTM export GTM-MNRP4PF_workspace247.json.
User data mapping uses user_data.billing_*, while samples show user_data.email/user_data.phone; email/phone likely drop. Source: wGTM export GTM-MNRP4PF_workspace247.json, messer datalayers new.txt.
Server endpoint uses gtm_server_domain https://messerattach.com/metrics with a Cloudflare Worker rewriting /metrics/ to sgtm.messerattach.com; user indicates it is unchanged, but verify request logs since server-side hits are missing. Source: wGTM export GTM-MNRP4PF_workspace247.json, provided Cloudflare Worker snippet.
Client-side tags present: Google Tag proxying to /metrics, FB Pixel PageView, MS UET events, and LinkedIn Insight; no GA4 event tags. Source: wGTM export GTM-MNRP4PF_workspace247.json, Tag Assistant chunked_output/tag_assistant_messerattach_com_2025_12_24_messages_chunk_24.json.

Part 2: Server-Side Powerhouse - Data Client & sGTM

Data Client has generateClientId: true, prolongCookies: true, acceptMultipleEvents: true, but no explicit path settings visible in export. Source: sGTM export GTM-K3CQBMZ9_workspace36.json.
GA4 Client is missing; GA4 Advanced tags exist only for purchase and add_to_cart and are set to debug logging. Source: sGTM export GTM-K3CQBMZ9_workspace36.json.
Meta CAPI tags exist for view_item/add_to_cart/begin_checkout/purchase and require Data Client events. Source: sGTM export GTM-K3CQBMZ9_workspace36.json.
Google Ads conversion/remarketing tags are configured server-side; conversion linker is server-side as well. Source: sGTM export GTM-K3CQBMZ9_workspace36.json.
Templates for Cookie Restore and Microsoft Ads Offline Conversion are installed but not used. Source: sGTM export GTM-K3CQBMZ9_workspace36.json.

Part 3: Variables, Triggers, Tags

wGTM ecommerce DLVs match GA4-style keys (ecommerce.items/value/currency), but the checkout event uses currencyCode and non-GA4 item schema. Source: wGTM export GTM-MNRP4PF_workspace247.json, messer datalayers new.txt.
dlv - user_id reads user_data.user_id, yet data layer uses top-level user_id; value is null in user_data pushes. Source: wGTM export GTM-MNRP4PF_workspace247.json, messer datalayers new.txt.
sGTM triggers filter on Client Name = Data Client, so only Data Tag payloads trigger tags; Data Tag currently only fires purchase. Source: sGTM export GTM-K3CQBMZ9_workspace36.json, wGTM export GTM-MNRP4PF_workspace247.json.
Event ID alignment is inconsistent: Data Tag uses Unique Event ID, while Pixel and sGTM use gtm.uniqueEventId. Source: wGTM export GTM-MNRP4PF_workspace247.json, sGTM export GTM-K3CQBMZ9_workspace36.json.
msclkid variable exists but is not used or stored. Source: wGTM export GTM-MNRP4PF_workspace247.json.

Part 4: Consent Mode v2

Consent default is denied and update grants ad_storage/analytics_storage/ad_user_data/ad_personalization. Source: Tag Assistant chunked_output/tag_assistant_messerattach_com_2025_12_24_messages_chunk_24.json.
Data Tag is set to consentStatus: NOT_NEEDED and will fire regardless of consent. Source: wGTM export GTM-MNRP4PF_workspace247.json.
sGTM tags have consentStatus: NOT_SET; GA4/Ads tags are not explicitly gated by consent. Source: sGTM export GTM-K3CQBMZ9_workspace36.json.
ads_data_redaction is false in event payloads. Source: Tag Assistant chunked_output/tag_assistant_messerattach_com_2025_12_24_messages_chunk_24.json.

Part 5: Data Integrity, Accuracy, Security

Current flow is fragmented: gtag hits go to /metrics/g/collect while Data Tag only sends purchase to /data, and sGTM lacks GA4 Client. Source: Tag Assistant chunked_output/tag_assistant_messerattach_com_2025_12_24_messages_chunk_24.json, wGTM export GTM-MNRP4PF_workspace247.json, sGTM export GTM-K3CQBMZ9_workspace36.json.
Same-origin Cloudflare Worker proxies /metrics/ to sgtm.messerattach.com by rewriting the path and Host header; user indicates it is unchanged, but missing server-side logs still warrant verifying worker routing and Cloudflare request logs. Source: provided Cloudflare Worker snippet.
Dedup risk exists if client and server events are both active without aligned event_id values. Source: wGTM export GTM-MNRP4PF_workspace247.json, sGTM export GTM-K3CQBMZ9_workspace36.json.
add_data_layer can pass raw PII (email/phone), which conflicts with stated hashing strategy. Source: wGTM export GTM-MNRP4PF_workspace247.json, messer datalayers new.txt.
Provided Stape log file appears to be control-plane API logs (/stape-api/...), not sGTM hit logs; no /data or /g/collect entries are visible, and sGTM hit logs are missing. Source: stape io logs messer.csv, tag_assistant_sgtm_messerattach_com_2025_12_24.json.
GA4/Meta server tags are set to debug logging, adding overhead in production. Source: sGTM export GTM-K3CQBMZ9_workspace36.json.

WooCommerce Specific Insights

view_item/view_item_list/add_to_cart/begin_checkout/view_cart data layer events are present with items/value/currency, which is a good base. Source: Tag Assistant chunked_output/tag_assistant_messerattach_com_2025_12_24_messages_chunk_24.json, messer datalayers new.txt.
checkout event uses ecommerce.currencyCode and non-GA4 item schema; avoid routing that event directly to GA4. Source: messer datalayers new.txt.
user_data pushes happen repeatedly on input (keyup), which can spam PII into dataLayer if not filtered. Source: messer datalayers new.txt.
Purchase event data was not provided, so purchase schema validation is pending. Source: messer datalayers new.txt.

Change Log / Audit Trail

Both exports show containerVersionId: 0 and no version name, indicating draft/preview rather than published versions. Source: GTM-MNRP4PF_workspace247.json, GTM-K3CQBMZ9_workspace36.json.
Export times are within the same minute on 2025-12-24, suggesting a single snapshot. Source: same files.
sGTM container is GTM-K3CQBMZ9 (SERVER) and wGTM container is GTM-MNRP4PF (WEB). Source: same files.
sGTM Tag Assistant file has zero messages (preview-only state). Source: tag_assistant_sgtm_messerattach_com_2025_12_24.json.

Limitations / Gaps

Requested exports GTM-5QFH6NXN.json and GTM-K3CQBMZ9.json are not present; analysis uses workspace exports GTM-K3CQBMZ9_workspace36.json (sGTM) and GTM-MNRP4PF_workspace247.json (wGTM). Source: local file inventory.
AI-optimized Tag Assistant bundle includes only GTM-MNRP4PF and GT-NS9Z5FWG; no sGTM container data is present. Source: chunked_output/full file/ai-optimized/1_summary.json.
No purchase data layer example or Tag Assistant purchase trace to validate transaction_id/value/items. Source: messer datalayers new.txt.
sGTM Tag Assistant recording contains no events, so server-side tag firing cannot be confirmed. Source: tag_assistant_sgtm_messerattach_com_2025_12_24.json.
Stape logs do not show /data or /g/collect traffic, limiting server-side verification. Source: stape io logs messer.csv.
The full wGTM Tag Assistant file in chunked_output/full file/tag_assistant_messerattach_com_2025_12_24.json contains container metadata but no event messages; event evidence is taken from chunked_output/tag_assistant_messerattach_com_2025_12_24_messages_chunk_*.json. Source: chunked_output/full file/tag_assistant_messerattach_com_2025_12_24.json, chunked_output/tag_assistant_messerattach_com_2025_12_24_messages_chunk_24.json.
No diagram provided; routing assumptions are based solely on exports and Tag Assistant. Source: not provided.

Actionable Recommendations - Critical (Impact: High / Effort: Low-Medium)

Expand Data Tag triggers to all ecommerce events and page_view, and add GA4 Advanced tags for view_item/view_item_list/view_cart/begin_checkout/add_payment_info/add_shipping_info/purchase. Source basis: wGTM export GTM-MNRP4PF_workspace247.json, sGTM export GTM-K3CQBMZ9_workspace36.json.
Fix User-ID mapping: add DLV for top-level user_id, pass raw to sGTM, and set GA4 user_id parameter (not user property). Source basis: messer datalayers new.txt, wGTM/sGTM exports.
Decide GA4 routing: either re-enable GA4 Client in sGTM for /metrics/g/collect or remove server_container_url to send GA4 direct; do not leave GA4 client removed while proxying. Source basis: Tag Assistant chunked_output/tag_assistant_messerattach_com_2025_12_24_messages_chunk_24.json, sGTM export GTM-K3CQBMZ9_workspace36.json.
Standardize event_id for dedup (use gtm.uniqueEventId consistently across browser pixel and CAPI). Source basis: wGTM export GTM-MNRP4PF_workspace247.json, sGTM export GTM-K3CQBMZ9_workspace36.json.
Add GA4 item mapping for all ecommerce events (items/value/currency/transaction_id) to ensure server-side GA4 completeness. Source basis: sGTM export GTM-K3CQBMZ9_workspace36.json.

Actionable Recommendations - High (Impact: High / Effort: Medium)

Disable add_data_layer or add allowlist/redaction in sGTM to prevent raw PII from passing through. Source basis: wGTM export GTM-MNRP4PF_workspace247.json, messer datalayers new.txt.
Update user_data mapping to user_data.email and user_data.phone (or add fallbacks) before hashing. Source basis: wGTM export GTM-MNRP4PF_workspace247.json, messer datalayers new.txt.
Implement msclkid storage and pass-through in Data Tag custom_data for Microsoft Ads. Source basis: wGTM export GTM-MNRP4PF_workspace247.json.
Apply consent gating in sGTM for GA4/Ads tags using analytics_storage/ad_storage checks. Source basis: sGTM export GTM-K3CQBMZ9_workspace36.json.
Turn off debug logType on server tags in production. Source basis: sGTM export GTM-K3CQBMZ9_workspace36.json.

Actionable Recommendations - Medium/Low

Add Cookie Restore tag if you want longer-lived first-party identifiers. Source basis: sGTM export GTM-K3CQBMZ9_workspace36.json.
Review MS UET event tags using PAGE_LOAD tracking for action events; align to event-based triggers. Source basis: wGTM export GTM-MNRP4PF_workspace247.json.
Remove or implement unused variables/templates (e.g., GA4 - ID, User-Provided Data, Microsoft Ads Offline template). Source basis: wGTM/sGTM exports.
Validate purchase event schema in WooCommerce and ensure it feeds GA4/Ads/CAPI. Source basis: messer datalayers new.txt.

Suggested Next Steps

Confirm the intended GA4 routing path (Data Tag -> sGTM Data Client vs Google Tag -> sGTM GA4 Client) so I can outline a minimal-change fix.
Provide a purchase dataLayer sample or Tag Assistant purchase trace to validate transaction_id/value/items/user_data.
Run a fresh sGTM preview while triggering view_item/add_to_cart/begin_checkout so we can verify Data Client ingestion and tag firing.

