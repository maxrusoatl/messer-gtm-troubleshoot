GTM AUDIT REPORT (Current Snapshot)

This report replaces legacy workspace247/36 findings. The current exports (workspace252/39) do not show the purchase-only Data Tag miswire.

Sources
- original-data/GTM-MNRP4PF_workspace252.json (wGTM)
- original-data/GTM-K3CQBMZ9_workspace39.json (sGTM)
- original-data/tag_assistant_messerattach_com_2026_01_08.json (web container messages)
- original-data/tag_assistant_sgtm_messerattach_com_2026_01_08.json (sGTM capture; zero messages)

Current State Summary
- Data Tag: ce_ecom (ID 307) -> https://messerattach.com/metrics/data
- Google Tag: server_container_url -> https://messerattach.com/metrics
- sGTM Data Client: present (Client Name filter for Data Client)
- GA4 server: GA4 Advanced fires on t_ecomCore
- Google Ads server: add_to_cart, begin_checkout, generate_lead, purchase + remarketing via Data Client
- Meta CAPI server: view_item, add_to_cart, begin_checkout, purchase
- LinkedIn CAPI: not configured in sGTM
- MS UET: view_item userDefined; add_to_cart/checkout/purchase are PAGE_LOAD

Coverage Snapshot
| Component | Current State | Notes |
| --- | --- | --- |
| Data Tag | ce_ecom (ID 307) -> /metrics/data | Validate payloads in preview |
| Google Tag | server_container_url -> /metrics | Confirm /g/collect handling |
| GA4 server | t_ecomCore | Verify in DebugView |
| Google Ads server | Conversion-focused | Add full-funnel events if needed |
| Meta CAPI server | Conversion-focused | Add full-funnel events if needed |
| LinkedIn CAPI | Not configured | Client-side Insight only |
| MS UET | Mixed PAGE_LOAD/userDefined | Consider userDefined for action events |

Validation Checklist
1) Confirm /metrics and /metrics/data hits in sGTM preview or logs.
2) Validate Data Tag custom_data (items, value, currency, transaction_id, event_id).
3) Review user_id mapping and hashing strategy for GA4 vs ads.
4) Review consent requirements across wGTM and sGTM tags.
5) Decide on expanding server-side coverage beyond conversions.

Open Gaps
- sGTM Tag Assistant capture has zero messages; server-side tag firing needs a fresh preview session.
- add_data_layer is enabled; audit the dataLayer for raw PII exposure.

Next Actions
- Capture a fresh sGTM Tag Assistant session.
- Validate event payloads and dedup strategy.
- Expand Ads/CAPI server triggers if full-funnel coverage is required.
