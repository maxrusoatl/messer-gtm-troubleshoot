SOP Contract Summary

sGTM client claim: Data Client template states default path /data and Data Client config shows no additional path parameters. (GTM-K3CQBMZ9_workspace40.json)
Cloudflare Worker: forwards to https://sgtm.messerattach.com and rewrites pathname.replace('/metrics/', '/'). (cloudflare worker sop metrix -sgtm.js)
Match/Mismatch: /metrics/data should map to /data (match), but /metrics/281sqstbcsp maps to /281sqstbcsp (not /data); both requests show 400 in the console capture. (begin checkout chrome console.md)
Executive Summary

/metrics collection is failing in-browser: POST /metrics/data?v=2&event=begin_checkout is 400, and the Google Tag /metrics/281... (decoded /g/collect page_view) is also 400; sGTM preview export contains no messages to confirm ingestion. (begin checkout chrome console.md, tag_assistant_sgtm_messerattach_com_2026_01_15.json)
event_id is missing in DataLayer samples and the wGTM Data Tag does not map it; sGTM expects event_id but there is no evidence it is populated, so dedupe is unreliable. (new view_iteam data layer.json, new begin checkout data layer.json, messer purchase datalayer.json, GTM-MNRP4PF_workspace253.json, GTM-K3CQBMZ9_workspace40.json)
sGTM GA4 duplication risk exists because Tag/GA4 Advanced fires on a regex that includes add_to_cart while Tag/GA4 ADV add_to_cart also fires on add_to_cart. (GTM-K3CQBMZ9_workspace40.json)
Top fixes: fix /metrics 400 (client claim + GA4 client for /g/collect or disable gtag), add event_id mapping end‑to‑end, and de‑duplicate GA4 tags; validate with sGTM preview and 2xx /metrics. (GTM-MNRP4PF_workspace253.json, GTM-K3CQBMZ9_workspace40.json, begin checkout chrome console.md)
Current Situation Map

Consent: Complianz tag triggers gtag.consent.update with wasSetLate: true; Data Tag template adds consent_state; DataLayer pushes cmplz_event_* events. (tag_assistant_messerattach_com_2026_01_15.json, GTM-MNRP4PF_workspace253.json, new view_iteam data layer.json)
wGTM: Data Tag fires on view_item, add_to_cart, view_item_list, view_cart, begin_checkout, purchase; ms_uet_* tags fire on their respective ecommerce events. (tag_assistant_messerattach_com_2026_01_15.json)
Network: POST /metrics/data for begin_checkout returns 400; GET /metrics/281... (decoded /g/collect page_view) returns 400; preview params appear on metrics/?gtm_debug=... loads. (begin checkout chrome console.md)
sGTM ingestion: Tag Assistant sGTM export has zero messages/logs; Stape logs show Debug/Custom Script Load/Cookie Keeper/Store only. (tag_assistant_sgtm_messerattach_com_2026_01_15.json, stape io messer logs.csv)
sGTM outbound: GA4 Advanced, GA4 ADV add_to_cart, Google Ads conversion + remarketing, and FB CAPI tags are configured. (GTM-K3CQBMZ9_workspace40.json)
Parallel sends: client-side FB Pixel, LinkedIn Insight, Microsoft UET, Google Ads calls, Mailchimp, Click Cease, and Google Tag (GT‑NS9Z5FWG) with mPath=/metrics. (GTM-MNRP4PF_workspace253.json, tag_assistant_messerattach_com_2026_01_15.json)
Edge config: Worker code exists; Cloudflare rules/DNS/WP Rocket settings are not provided. (cloudflare worker sop metrix -sgtm.js)
Inventory Table

ID/Key	Template/Type	Where used
GTM-MNRP4PF	Web GTM container	wGTM export container. (GTM-MNRP4PF_workspace253.json)
GTM-K3CQBMZ9	Server GTM container	sGTM export container. (GTM-K3CQBMZ9_workspace40.json)
GT-NS9Z5FWG	Google Tag (googtag)	wGTM Tag/Google Tag; GTAG container with mPath=/metrics. (GTM-MNRP4PF_workspace253.json, tag_assistant_messerattach_com_2026_01_15.json)
G‑YCL5FGZNCV	GA4 Measurement ID	wGTM Variable/GA4 - ID; sGTM Tags/GA4 Advanced + GA4 ADV add_to_cart use {{GA4 - ID}}. (GTM-MNRP4PF_workspace253.json, GTM-K3CQBMZ9_workspace40.json)
767740215	Google Ads Conversion ID	wGTM google_ads_calls + google_ads_800calls; sGTM Google Ads conversion/remarketing tags. (GTM-MNRP4PF_workspace253.json, GTM-K3CQBMZ9_workspace40.json)
ZLAFCNKDkusYELeSi-4C / WrSjCJnAiesYELeSi-4C	Google Ads call labels	wGTM google_ads_calls / google_ads_800calls. (GTM-MNRP4PF_workspace253.json)
srU-CMOM3OoYELeSi-4C / y0V4CNzM0uoYELeSi-4C / gM6CCLv40eoYELeSi-4C / oFJkCJX62uoYELeSi-4C	Google Ads conversion labels	sGTM begin_checkout / add_to_cart / purchase / generate_lead tags. (GTM-K3CQBMZ9_workspace40.json)
3695834564032094	Facebook Pixel ID	wGTM FB - Page View; sGTM FB CAPI tags. (GTM-MNRP4PF_workspace253.json, GTM-K3CQBMZ9_workspace40.json)
4898740	LinkedIn Insight ID	wGTM LinkedIn Insight tag. (GTM-MNRP4PF_workspace253.json)
343101821	Microsoft UET ID	wGTM ms_uet_* tags + ms_ads variable. (GTM-MNRP4PF_workspace253.json)
https://messerattach.com/metrics + /data	Stape Data Tag endpoint	wGTM Tag/Data Tag gtm_server_domain + request_path. (GTM-MNRP4PF_workspace253.json)
/data (default)	Data Client claim path	sGTM Data Client template default path. (GTM-K3CQBMZ9_workspace40.json)
sgtm.messerattach.com	Worker upstream host	Cloudflare Worker domain + Host override. (cloudflare worker sop metrix -sgtm.js)
Keypath Map Table

Field	DataLayer keypath	wGTM variable	Stape Data Tag field	/metrics payload key	sGTM eventData keypath	sGTM tag field mapping
event_id	Not present in samples	Unique Event ID	Not configured	Not determinable	event_id	Not determinable
user_id	user_id (user_init only)	dlv - user_id	add_data_layer	Not determinable	user_id	Google Ads Remarketing uses EVENT_DATA userId
transaction_id	ecommerce.transaction_id	dlv_transactionID	add_data_layer	Not determinable	transaction_id	Not determinable
items	ecommerce.items	dlv_ecommerce_items	add_data_layer	Not determinable	items	GA4 Advanced uses eventData; Ads product reporting uses EVENT
value	ecommerce.value	dlv_value	add_data_layer	Not determinable	value	Google Ads conversionValue uses EDV_ecommerce.value
currency	ecommerce.currency	dlv_ecommerce_currency	add_data_layer	Not determinable	currency	Google Ads currencyCode uses EDV_ecommerce.currency
consent_state	Not in DataLayer	N/A	add_consent_state	consent_state (template help)	Not determinable	Not determinable
gcd	N/A	N/A	N/A	gcd in /g/collect	Not determinable	Not determinable
record	Not determinable	Not determinable	Not determinable	Not determinable	Not determinable	Not determinable
Evidence for keypaths and mappings: DataLayer samples (new view_iteam data layer.json, new cart view.json, new begin checkout data layer.json, messer view list datalayer.json, messer purchase datalayer.json), wGTM variables/Data Tag config (GTM-MNRP4PF_workspace253.json), Data Tag template consent_state help (GTM-MNRP4PF_workspace253.json), sGTM EDV variables + tag params (GTM-K3CQBMZ9_workspace40.json), /g/collect gcd in console (begin checkout chrome console.md), Unique Event ID template (unique even id template stape io.js).

Tag/Trigger Matrix (wGTM)

wGTM tag	Trigger	event_name / condition
LinkedIn Insight	CM - All Consent Granted - Page View (PAGEVIEW)	PAGEVIEW trigger
FB - Page View	Built-in trigger ID 2147479572	Not determinable from export
Google Tag	Built-in trigger ID 2147479573	Not determinable from export
google_ads_calls	Built-in trigger ID 2147479572	Not determinable from export
google_ads_800calls	Built-in trigger ID 2147479572	Not determinable from export
Conversion Linker	Built-in trigger ID 2147479553	Not determinable from export
ms_uet_base	Built-in trigger ID 2147479572	Not determinable from export
ms_uet_view_item	ce_view_item	view_item
ms_uet_add_to_cart	ce_add_to_cart	add_to_cart
ms_uet_checkout	ce_checkout	begin_checkout
ms_uet_purchase	ce_purchase	purchase
ms_uet_site_search	ce_ site_search	site_search
Data Tag	ce_ecom	regex includes view_item/add_to_cart/begin_checkout/purchase/view_cart/view_item_list
Helper - Push search Event	Page View - Search Results (DOM_READY)	Page URL matches ?s=.+, pushes event: search
Mailchimp	CM - All Consent Granted - Page View (PAGEVIEW)	PAGEVIEW trigger
Click Cease	CM - All Consent Granted - Page View (PAGEVIEW)	PAGEVIEW trigger
Complianz.io - The Privacy Suite for WordPress	Built-in trigger ID 2147479572	Not determinable from export
Evidence: wGTM export tags and triggers. (GTM-MNRP4PF_workspace253.json)

Evidence Index / Coverage Summary

event_name	event_id	timestamp	page_url	source
view_item	124	Not determinable	https://messerattach.com/product/test-product/	wGTM Tag Assistant
add_to_cart	259	Not determinable	https://messerattach.com/product/test-product/	wGTM Tag Assistant
view_item_list	171	Not determinable	https://messerattach.com/product-category/attachments/bale-handling-made-easy/	wGTM Tag Assistant
view_cart	124	Not determinable	https://messerattach.com/cart/	wGTM Tag Assistant
begin_checkout	124	Not determinable	https://messerattach.com/checkout/	wGTM Tag Assistant
purchase	124	Not determinable	https://messerattach.com/checkout/order-received/17236/?key=wc_order_YhHVqpr2R0Ift	wGTM Tag Assistant
Evidence: event_name, event_id, and page_url from wGTM Tag Assistant. (tag_assistant_messerattach_com_2026_01_15.json)

sGTM Tag Assistant has 0 messages/logs; no inbound event evidence. (tag_assistant_sgtm_messerattach_com_2026_01_15.json)
Stape logs show only Debug/Custom Script Load/Cookie Keeper/Store entries; no event hits. (stape io messer logs.csv)
Event Chain Results Table

Event	DataLayer payload	wGTM Data Tag fired once	/metrics request sent	sGTM client ingestion	sGTM GA4 tag fired	sGTM Ads tag fired
view_item	PASS	PASS	Not determinable	Not determinable	Not determinable	Not determinable
add_to_cart	Not determinable	PASS	Not determinable	Not determinable	Not determinable	Not determinable
view_item_list	PASS	PASS	Not determinable	Not determinable	Not determinable	Not determinable
view_cart	PASS	PASS	Not determinable	Not determinable	Not determinable	Not determinable
begin_checkout	PASS	PASS	FAIL (400)	Not determinable	Not determinable	Not determinable
purchase	PASS	PASS	Not determinable	Not determinable	Not determinable	Not determinable
Evidence: DataLayer samples for view_item/view_item_list/view_cart/begin_checkout/purchase (new view_iteam data layer.json, messer view list datalayer.json, new cart view.json, new begin checkout data layer.json, messer purchase datalayer.json); wGTM Data Tag firing from Tag Assistant (tag_assistant_messerattach_com_2026_01_15.json); /metrics 400 for begin_checkout (begin checkout chrome console.md).

Root Causes (by layer) + Exact Fixes

DataLayer: event_id missing; user_id not present on ecommerce events; value/price are strings; purchase user_data includes raw PII (email/phone/address). (new view_iteam data layer.json, new begin checkout data layer.json, messer purchase datalayer.json)
Fix: inject event_id on every ecommerce event (use Unique Event ID variable), include user_id on ecommerce events, cast numeric fields to numbers, and hash/limit PII before pushing. (unique even id template stape io.js)
wGTM: Data Tag sends to /metrics/data but does not map event_id; /metrics POST returns 400 for begin_checkout. (GTM-MNRP4PF_workspace253.json, begin checkout chrome console.md)
Fix: map Unique Event ID into Data Tag (custom_data or event_id field), verify payload shape and Content-Type; re‑test until /metrics returns 2xx.
/metrics + Worker: Worker rewrites /metrics/ to /; /metrics/data and /metrics/281... return 400; Data Client defaults to /data, so /metrics/281... (decoded /g/collect) is not claimed. (cloudflare worker sop metrix -sgtm.js, begin checkout chrome console.md, GTM-K3CQBMZ9_workspace40.json)
Fix: add GA4 client for /g/collect or stop Google Tag from sending GA4 hits via /metrics if not needed; add guard for /metrics without trailing slash; add logging for non‑2xx.
sGTM: Preview export is empty; GA4 tags overlap on add_to_cart. (tag_assistant_sgtm_messerattach_com_2026_01_15.json, GTM-K3CQBMZ9_workspace40.json)
Fix: verify preview headers reach sGTM (x-gtm-server-preview, etc), and de‑duplicate GA4 tags by removing or narrowing GA4 ADV add_to_cart.
Critical Issue: GA4 Ecommerce Missing/Unreliable

Confirmed failure layers: /metrics requests are 400 and sGTM preview is empty, so ingestion and GA4 tag firing are not proven. (begin checkout chrome console.md, tag_assistant_sgtm_messerattach_com_2026_01_15.json)
Fix: align Data Client /data ingestion and add a GA4 client or disable gtag /g/collect gateway, then validate with sGTM preview + GA4 DebugView. (GTM-K3CQBMZ9_workspace40.json)
Purchase test plan: run controlled purchase with Tag Assistant wGTM + sGTM preview, verify /metrics 2xx, Data Client claim, GA4 tag firing, and GA4 DebugView receipt.
Critical Issue: event_id Missing/Unreliable

Mapping chain: DataLayer has no event_id; Unique Event ID variable exists but Data Tag does not map it; sGTM expects event_id. (new view_iteam data layer.json, GTM-MNRP4PF_workspace253.json, unique even id template stape io.js, GTM-K3CQBMZ9_workspace40.json)
Break point: wGTM Data Tag payload lacks event_id.
Fix: map {{Unique Event ID}} into Data Tag as event_id, ensure Data Client passes to eventData, and map to GA4/Ads/Meta tags.
Critical Issue: sGTM Preview Empty but Logs Show Hits

Evidence: sGTM Tag Assistant has no messages and Stape logs show no event hits. (tag_assistant_sgtm_messerattach_com_2026_01_15.json, stape io messer logs.csv)
Root cause: Not determinable from provided inputs; likely preview header passthrough or client claim mismatch.
Fix: confirm preview headers on /metrics requests; adjust Worker/header transforms to preserve them; re‑capture sGTM preview.
Critical Issue: GA4 user_id Not Appearing

Mapping chain: DataLayer user_id exists only on user_init; wGTM variable exists; sGTM expects user_id. (new view_iteam data layer.json, GTM-MNRP4PF_workspace253.json, GTM-K3CQBMZ9_workspace40.json)
Break point: user_id not present on ecommerce events.
Fix: persist user_id at top-level before ecommerce events or inject into each ecommerce push; validate in sGTM preview.
Consent Timing vs Event Timing

Tag Assistant shows consent updates before ecommerce events within each group but wasSetLate: true is flagged. (tag_assistant_messerattach_com_2026_01_15.json)
Fix: ensure Complianz consent update fires before ecommerce pushes (delay events or move consent updates earlier); validate ordering in Tag Assistant.
Routing Classification + Duplication Controls

Proven send paths:
wGTM Data Tag -> /metrics/data -> Worker -> Data Client -> sGTM tags (configured). (GTM-MNRP4PF_workspace253.json, GTM-K3CQBMZ9_workspace40.json, cloudflare worker sop metrix -sgtm.js)
Google Tag (GT‑NS9Z5FWG) -> /metrics/281... -> decoded /g/collect page_view (400). (begin checkout chrome console.md, tag_assistant_messerattach_com_2026_01_15.json)
Client-side pixels/utilities: FB Pixel, LinkedIn Insight, Microsoft UET, Google Ads call conversions, Mailchimp, Click Cease. (GTM-MNRP4PF_workspace253.json)
gtag classification: gtag present routed via gateway/SOP; only /metrics path is observed and no direct Google endpoints are shown in provided logs. (tag_assistant_messerattach_com_2026_01_15.json, begin checkout chrome console.md)
Routing per destination:
GA4 ecommerce: Not determinable from provided inputs; server-side tags are configured, but gtag is also present via /metrics. (GTM-K3CQBMZ9_workspace40.json, tag_assistant_messerattach_com_2026_01_15.json)
Google Ads conversions: server-side for add_to_cart/begin_checkout/purchase/generate_lead; client-side for call conversions. (GTM-K3CQBMZ9_workspace40.json, GTM-MNRP4PF_workspace253.json)
Microsoft Ads (UET): client-only. (GTM-MNRP4PF_workspace253.json)
Meta: hybrid (FB Pixel client + FB CAPI server). (GTM-MNRP4PF_workspace253.json, GTM-K3CQBMZ9_workspace40.json)
LinkedIn Insight: client-only. (GTM-MNRP4PF_workspace253.json)
Mailchimp: client-only. (GTM-MNRP4PF_workspace253.json)
Remarketing: server-side Google Ads Remarketing tag configured. (GTM-K3CQBMZ9_workspace40.json)
Keep / Disable / Move server-side:
Keep client-side: google_ads_calls, google_ads_800calls (call tracking), Click Cease (fraud), Mailchimp (utility), LinkedIn/FB Pixel (audience signals) as explicit exceptions. (GTM-MNRP4PF_workspace253.json)
Consider disabling or scoping Google Tag if GA4 ecommerce is server‑side only to avoid hybrid duplication. (GTM-MNRP4PF_workspace253.json)
Dedup rule: event_id must be consistent across any hybrid path.
Consent + PII Findings

Consent Mode v2 signals exist in gtag payload (gcd, gcs) and Data Tag template can add consent_state, but consent update flags wasSetLate: true. (begin checkout chrome console.md, GTM-MNRP4PF_workspace253.json, tag_assistant_messerattach_com_2026_01_15.json)
Purchase DataLayer contains raw PII (email/phone/address); ms_uet_base uses Customers Email/Phone DLVs, which are not hashed. (messer purchase datalayer.json, GTM-MNRP4PF_workspace253.json)
user_data is empty on view_item and begin_checkout samples, so PII propagation for earlier funnel events is not shown. (new view_iteam data layer.json, new begin checkout data layer.json)
SOP Findings + Hardening Actions

Cache bypass, WAF/Bot exemptions, and DNS routing for /metrics/* are not determinable from provided inputs; these must be verified in Cloudflare and WP Rocket. (Not determinable)
Worker should preserve method/body and explicitly allowlist preview headers; add guard for /metrics (no trailing slash) to avoid path loss. (cloudflare worker sop metrix -sgtm.js)
Add lightweight logging/alerts for non‑2xx responses on /metrics/* to catch 400s quickly. (begin checkout chrome console.md)
Prioritized Action Plan

Critical | Effort M | Fix /metrics 400: ensure Data Client claims /data, add GA4 client for /g/collect or disable Google Tag, and update Worker for /metrics edge cases; Validate: /metrics returns 2xx and sGTM preview shows Data Client claim + GA4 tag firing. (GTM-K3CQBMZ9_workspace40.json, cloudflare worker sop metrix -sgtm.js, begin checkout chrome console.md)
Critical | Effort S | Add event_id end‑to‑end: map {{Unique Event ID}} into Data Tag as event_id and confirm it reaches sGTM EDV - event_id; Validate: event_id visible in sGTM preview and GA4/Ads tags. (unique even id template stape io.js, GTM-MNRP4PF_workspace253.json, GTM-K3CQBMZ9_workspace40.json)
High | Effort S | De‑duplicate GA4: remove GA4 ADV add_to_cart or exclude add_to_cart from GA4 Advanced; Validate: only one GA4 server tag fires on add_to_cart. (GTM-K3CQBMZ9_workspace40.json)
High | Effort S | Consent timing: ensure consent update precedes ecommerce events and clear wasSetLate; Validate in Tag Assistant. (tag_assistant_messerattach_com_2026_01_15.json)
Medium | Effort M | PII handling: hash or exclude PII before GA4; restrict raw user_data to allowed destinations; Validate with sGTM preview payload inspection. (messer purchase datalayer.json)
Low | Effort S | SOP hardening: add Cloudflare cache bypass/WAF exemptions and preview‑header allowlist; Validate with /metrics requests carrying preview headers. (cloudflare worker sop metrix -sgtm.js)
Evidence Gaps / Required Inputs

sGTM preview export with live ecommerce events (client claim + tag firing details).
Network HAR for /metrics requests (method, Content-Type, payload, x-gtm-server-preview headers).
Cloudflare Worker route, header transform rules, cache/WAF/Bot settings, and DNS records for messerattach.com/sgtm.
WP Rocket exclusions for /metrics/*.
Stape logs with event hits (event_name/event_id/path/status) for /data ingestion.
If you want, I can generate the exact change checklist (Worker adjustments + GTM edits) once you provide the missing inputs.