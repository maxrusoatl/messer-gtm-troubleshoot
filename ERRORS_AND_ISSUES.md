# Errors and Issues (Current Snapshot)

Updated: 2026-01-08

This file replaces the 2024 legacy error log. For full context and current visuals, use:
- audit-report.md
- GTM_AUDIT_REPORT.md

## Confirmed issues (current evidence)
- SOP observability gap: no /metrics network capture and sGTM Tag Assistant recording contains zero messages.
  Evidence: original-data/tag_assistant_sgtm_messerattach_com_2026_01_08.json
- Consent gating not configured: wGTM Data Tag consentStatus is NOT_NEEDED; sGTM tags consentStatus are NOT_SET.
  Evidence: original-data/GTM-MNRP4PF_workspace252.json, original-data/GTM-K3CQBMZ9_workspace39.json
- user_id mapping mismatch: DataLayer uses top-level user_id; sGTM EDV - user_id reads user_data.user_id; user_data is empty in samples.
  Evidence: original-data/new begin checkout data layer.json, original-data/GTM-K3CQBMZ9_workspace39.json
- Data quality gaps: value/price/cart_total are strings; ecomm_pagetype is basket on cart/checkout.
  Evidence: original-data/new cart view.json, original-data/new begin checkout data layer.json
- sGTM GA4 overlap: GA4 Advanced fires on t_ecomCore (includes add_to_cart) while GA4 ADV add_to_cart also fires on add_to_cart.
  Evidence: original-data/GTM-K3CQBMZ9_workspace39.json

## Non-issues / corrected legacy claims
- No purchase-only miswire in current exports: wGTM Data Tag fires on ce_ecom (ID 307).
  Evidence: original-data/GTM-MNRP4PF_workspace252.json
