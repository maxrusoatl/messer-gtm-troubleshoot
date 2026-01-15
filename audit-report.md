Audit Report (Current Snapshot)

Sources
- original-data/GTM-MNRP4PF_workspace252.json (wGTM)
- original-data/GTM-K3CQBMZ9_workspace39.json (sGTM)
- original-data/tag_assistant_messerattach_com_2026_01_08.json (web container messages)
- original-data/tag_assistant_sgtm_messerattach_com_2026_01_08.json (sGTM capture; zero messages)

Executive Summary
- Data Tag (tagId 310) uses ce_ecom (ID 307) and sends to https://messerattach.com/metrics/data. Core + ecommerce events are configured; verify payloads in sGTM preview/logs.
- Google Tag (GT-NS9Z5FWG) sets server_container_url to https://messerattach.com/metrics; confirm /metrics routing to sGTM and GTM Web Container client handling of /g/collect.
- sGTM Data Client is present; GA4 Advanced fires on t_ecomCore. Ads/CAPI server tags are conversion-focused: Google Ads (add_to_cart, begin_checkout, generate_lead, purchase + remarketing via Data Client) and Meta CAPI (view_item, add_to_cart, begin_checkout, purchase). LinkedIn CAPI is not configured.
- add_data_layer is enabled in the Data Tag; audit the dataLayer for raw PII exposure and confirm user_data hashing strategy.
- sGTM Tag Assistant capture has zero messages, so server-side tag firing cannot be confirmed without a fresh preview session.

Key Validation Tasks
1) Validate /metrics and /metrics/data traffic in sGTM preview or logs.
2) Confirm event parameters (items, value, currency, transaction_id, event_id) in Data Tag payloads.
3) Verify user_id mapping for GA4 vs ads (unhashed for GA4, hashed for ads).
4) Decide whether to expand server-side events beyond conversions (view_cart, view_item_list, page_view).
5) Update MS UET tags to userDefined for add_to_cart/checkout/purchase if accuracy is required.

Notes
- Data Tag custom_data includes transaction_id, value, currency, items, event_id, fbp, fbc, search_term.
- MS UET view_item is userDefined; add_to_cart, checkout, purchase are PAGE_LOAD.
