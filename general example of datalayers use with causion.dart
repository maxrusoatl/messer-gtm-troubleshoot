[
  { "0": "set", "1": "developer_id.dYzg1YT", "2": true },

  /* ---------------------------
     PAGE LOAD / CONSENT / IDENTITY
  ---------------------------- */
  { "gtm.start": 1766544561282, "event": "gtm.js", "gtm.uniqueEventId": 14 },

  { "event": "cmplz_event_functional", "timestamp": 1766544561300, "gtm.uniqueEventId": 20 },
  { "event": "cmplz_event_preferences", "timestamp": 1766544561310, "gtm.uniqueEventId": 21 },
  { "event": "cmplz_event_statistics",  "timestamp": 1766544561320, "gtm.uniqueEventId": 22 },
  { "event": "cmplz_event_marketing",   "timestamp": 1766544561330, "gtm.uniqueEventId": 23 },

  {
    "event": "user_init",
    "timestamp": 1766544561388,
    "gtm.uniqueEventId": 102,

    /* event_id = sha256(user_id|event|timestamp|gtm.uniqueEventId) */
    "event_id": "f08d58e4fff091c0a98d1a77c2ce4ee6e3302010c08265a215409a56b476efe8",

    "user_data": {
      "user_id": "guest_7240e4c9-5919-49c4-b9bb-47b8f94bb5fc",
      "is_logged_in": false,
      "customer_id": ""
    },

    "consent_state": {
      "marketing": true,
      "statistics": true,
      "ad_storage": "granted",
      "analytics_storage": "granted"
    },

    "marketing_ids": {
      "fbp": "fb.1.1766544561.1234567890",
      "fbc": "",
      "fbclid": "",
      "gclid": "",
      "gbraid": "",
      "wbraid": "",
      "msclkid": "",
      "li_fat_id": ""
    },

    "page_context": {
      "url": "https://messerattach.com/product-category/attachments/",
      "path": "/product-category/attachments/",
      "referrer": "",
      "title": "Attachments",
      "client_user_agent": "Mozilla/5.0 (...) Chrome/125.0.0.0 Safari/537.36"
    }
  },

  /* ============================================================
     LISTING PAGE — view_item_list (NO PII)
  ============================================================ */
  { "ecommerce": null },

  {
    "event": "view_item_list",
    "timestamp": 1766544561700,
    "gtm.uniqueEventId": 120,
    "event_id": "1fcf8047c9ea03f967fdcbbf598a83860b58aee9e08e4253a7aca347925e9e5b",

    "user_data": { "user_id": "guest_7240e4c9-5919-49c4-b9bb-47b8f94bb5fc" },

    "page_context": {
      "url": "https://messerattach.com/product-category/attachments/",
      "path": "/product-category/attachments/",
      "referrer": "",
      "title": "Attachments"
    },

    "ecommerce": {
      "currency": "USD",
      "item_list_id": "cat_attachments",
      "item_list_name": "Attachments Category",
      "items": [
        {
          "item_id": "1119",
          "item_name": "75\" Manure Fork Grapple",
          "item_brand": "Messer Attachments",
          "item_category": "Attachments",
          "price": 4245.00,
          "index": 1
        },
        {
          "item_id": "9359",
          "item_name": "84\" High Capacity Grapple",
          "item_brand": "Messer Attachments",
          "item_category": "Attachments",
          "price": 6495.00,
          "index": 2
        }
      ]
    },

    "microsoft_ads": {
      "uet_remarketing": {
        "ecomm_pagetype": "category",
        "ecomm_prodid": ["1119", "9359"],
        "ecomm_totalvalue": 0.00,
        "currency": "USD"
      }
    }
  },

  /* Optional but recommended: select_item (requires you to add trigger/tag support) */
  { "ecommerce": null },
  {
    "event": "select_item",
    "timestamp": 1766544561850,
    "gtm.uniqueEventId": 128,
    "event_id": "1457745896d267562b7edb14efa2f668a9736cfc04aec1efc7ecce71b75afe1c",
    "user_data": { "user_id": "guest_7240e4c9-5919-49c4-b9bb-47b8f94bb5fc" },

    "ecommerce": {
      "currency": "USD",
      "item_list_id": "cat_attachments",
      "item_list_name": "Attachments Category",
      "items": [
        {
          "item_id": "1119",
          "item_name": "75\" Manure Fork Grapple",
          "item_brand": "Messer Attachments",
          "item_category": "Attachments",
          "price": 4245.00,
          "index": 1,
          "quantity": 1
        }
      ]
    }
  },

  /* ============================================================
     PRODUCT PAGE — view_item (NO PII)
  ============================================================ */
  { "ecommerce": null },

  {
    "event": "view_item",
    "timestamp": 1766544562000,
    "gtm.uniqueEventId": 135,
    "event_id": "9a86b92940143e3bdf3596c35f982c916d0e95cf0e473fbdcfdab5228aa6c3ab",

    "user_data": { "user_id": "guest_7240e4c9-5919-49c4-b9bb-47b8f94bb5fc" },

    "page_context": {
      "url": "https://messerattach.com/product/75-manure-fork-grapple/",
      "path": "/product/75-manure-fork-grapple/",
      "referrer": "https://messerattach.com/product-category/attachments/",
      "title": "75\" Manure Fork Grapple"
    },

    "ecommerce": {
      "currency": "USD",
      "value": 4245.00,
      "items": [
        {
          "item_id": "1119",
          "item_name": "75\" Manure Fork Grapple",
          "item_brand": "Messer Attachments",
          "item_sku": "MFG75",
          "item_category": "Attachments",
          "price": 4245.00,
          "quantity": 1
        }
      ]
    },

    "platform_payloads": {
      "meta": {
        "event_name": "ViewContent",
        "event_time": 1766544562,
        "event_id": "9a86b92940143e3bdf3596c35f982c916d0e95cf0e473fbdcfdab5228aa6c3ab",
        "user_data": {
          "external_id": "guest_7240e4c9-5919-49c4-b9bb-47b8f94bb5fc",
          "fbp": "fb.1.1766544561.1234567890",
          "fbc": ""
        },
        "custom_data": {
          "currency": "USD",
          "value": 4245.00,
          "content_type": "product",
          "content_ids": ["1119"],
          "contents": [{ "id": "1119", "quantity": 1, "item_price": 4245.00 }]
        }
      },

      "microsoft_ads": {
        "uet_remarketing": {
          "ecomm_pagetype": "product",
          "ecomm_prodid": ["1119"],
          "ecomm_totalvalue": 4245.00,
          "currency": "USD"
        }
      }
    }
  },

  /* ============================================================
     ADD TO CART — add_to_cart (NO PII)
  ============================================================ */
  { "ecommerce": null },

  {
    "event": "add_to_cart",
    "timestamp": 1766544562600,
    "gtm.uniqueEventId": 150,
    "event_id": "88ea8d949c157993040b9b38c5e884ba951d46d3b5a453419eb282393b78332a",

    "user_data": { "user_id": "guest_7240e4c9-5919-49c4-b9bb-47b8f94bb5fc" },

    "cart_quantity": 1,
    "cart_total": 4245.00,

    "ecommerce": {
      "currency": "USD",
      "value": 4245.00,
      "items": [
        {
          "item_id": "1119",
          "item_name": "75\" Manure Fork Grapple",
          "item_brand": "Messer Attachments",
          "item_sku": "MFG75",
          "price": 4245.00,
          "quantity": 1
        }
      ]
    }
  },

  /* ============================================================
     CART PAGE — view_cart (NO PII, CART not BASKET)
  ============================================================ */
  { "ecommerce": null },

  {
    "event": "view_cart",
    "timestamp": 1766544563000,
    "gtm.uniqueEventId": 170,
    "event_id": "70be4e1727ef21d720d257ee63b27668151c1608b954065031d132ee4f8b5864",

    "user_data": { "user_id": "guest_7240e4c9-5919-49c4-b9bb-47b8f94bb5fc" },

    "cart_quantity": 2,
    "cart_total": 10740.00,

    "ecommerce": {
      "currency": "USD",
      "value": 10740.00,
      "items": [
        { "item_id": "1119", "item_name": "75\" Manure Fork Grapple", "price": 4245.00, "quantity": 1, "index": 1 },
        { "item_id": "9359", "item_name": "84\" High Capacity Grapple", "price": 6495.00, "quantity": 1, "index": 2 }
      ]
    },

    "microsoft_ads": {
      "uet_remarketing": {
        "ecomm_pagetype": "cart",
        "ecomm_prodid": ["1119", "9359"],
        "ecomm_totalvalue": 10740.00,
        "currency": "USD"
      }
    }
  },

  /* ============================================================
     CHECKOUT PAGE — begin_checkout (NO PII YET)
  ============================================================ */
  { "ecommerce": null },

  {
    "event": "begin_checkout",
    "timestamp": 1766544563300,
    "gtm.uniqueEventId": 180,
    "event_id": "d1d2da93ea8dabac72c638c4e60d6b8a8eb06888ecea14d3ce306199603a97c7",

    "user_data": { "user_id": "guest_7240e4c9-5919-49c4-b9bb-47b8f94bb5fc" },

    "cart_quantity": 2,
    "cart_total": 10740.00,

    "ecommerce": {
      "currency": "USD",
      "value": 10740.00,
      "items": [
        { "item_id": "1119", "item_name": "75\" Manure Fork Grapple", "price": 4245.00, "quantity": 1, "index": 1 },
        { "item_id": "9359", "item_name": "84\" High Capacity Grapple", "price": 6495.00, "quantity": 1, "index": 2 }
      ]
    }
  },

  /* ============================================================
     CHECKOUT USER INFO — checkout_userinfo (PII allowed ONLY here, validated only)
     NOTE: Do NOT send raw PII to GA4 tags.
  ============================================================ */
  {
    "event": "checkout_userinfo",
    "timestamp": 1766544563600,
    "gtm.uniqueEventId": 190,
    "event_id": "d01d2315e9b226a3aad3fc93a0fbe2b1f081604c2f890822934ed896fa924834",

    "consent_state": {
      "marketing": true,
      "statistics": true,
      "ad_storage": "granted",
      "analytics_storage": "granted"
    },

    "user_data": {
      "user_id": "guest_7240e4c9-5919-49c4-b9bb-47b8f94bb5fc",

      "billing_email": "customer@example.com",
      "phone_number": "15555550199",
      "billing_first_name": "Max",
      "billing_last_name": "Ruso",
      "billing_address": "123 Example St",
      "billing_city": "Tucker",
      "billing_state": "GA",
      "billing_postcode": "30084",
      "billing_country": "US",

      "shipping_first_name": "Max",
      "shipping_last_name": "Ruso",
      "shipping_address": "123 Warehouse Rd",
      "shipping_city": "Atlanta",
      "shipping_state": "GA",
      "shipping_postcode": "30303",
      "shipping_country": "US"
    },

    "platform_payloads": {
      "meta": {
        "user_data": {
          "em": "HASH_IN_SGTM",
          "ph": "HASH_IN_SGTM",
          "fn": "HASH_IN_SGTM",
          "ln": "HASH_IN_SGTM",
          "ct": "HASH_IN_SGTM",
          "st": "HASH_IN_SGTM",
          "zp": "HASH_IN_SGTM",
          "country": "HASH_IN_SGTM",
          "external_id": "guest_7240e4c9-5919-49c4-b9bb-47b8f94bb5fc"
        }
      }
    }
  },

  /* ============================================================
     SHIPPING — add_shipping_info
  ============================================================ */
  { "ecommerce": null },

  {
    "event": "add_shipping_info",
    "timestamp": 1766544563900,
    "gtm.uniqueEventId": 200,
    "event_id": "fc5ddbc0f98492ca75946a7c87f3bc39e1fc451df03778775694c1383db14340",

    "user_data": { "user_id": "guest_7240e4c9-5919-49c4-b9bb-47b8f94bb5fc" },

    "shipping_tier": "Freight",
    "shipping_method_id": "flat_rate:3",

    "ecommerce": {
      "currency": "USD",
      "value": 11239.00,
      "shipping": 499.00,
      "tax": 0.00,
      "items": [
        { "item_id": "1119", "item_name": "75\" Manure Fork Grapple", "price": 4245.00, "quantity": 1, "index": 1 },
        { "item_id": "9359", "item_name": "84\" High Capacity Grapple", "price": 6495.00, "quantity": 1, "index": 2 }
      ]
    }
  },

  /* ============================================================
     PAYMENT — add_payment_info (NO card_last4 in dataLayer)
  ============================================================ */
  { "ecommerce": null },

  {
    "event": "add_payment_info",
    "timestamp": 1766544564200,
    "gtm.uniqueEventId": 210,
    "event_id": "e75a628e98dce352b5de3eaa0db204bef0b1725dcbfdfff2dd369cc34f00b2ee",

    "user_data": { "user_id": "guest_7240e4c9-5919-49c4-b9bb-47b8f94bb5fc" },

    "payment_type": "credit_card",

    "ecommerce": {
      "currency": "USD",
      "value": 11239.00,
      "shipping": 499.00,
      "tax": 0.00,
      "items": [
        { "item_id": "1119", "item_name": "75\" Manure Fork Grapple", "price": 4245.00, "quantity": 1, "index": 1 },
        { "item_id": "9359", "item_name": "84\" High Capacity Grapple", "price": 6495.00, "quantity": 1, "index": 2 }
      ]
    }
  },

  /* ============================================================
     PURCHASE — purchase
  ============================================================ */
  { "ecommerce": null },

  {
    "event": "purchase",
    "timestamp": 1766544565000,
    "gtm.uniqueEventId": 220,
    "event_id": "f8597edc8c7d764fac2ee09beca91ce3e55ca4b288694c878ef4cc6d60852ac3",

    "user_data": { "user_id": "guest_7240e4c9-5919-49c4-b9bb-47b8f94bb5fc" },

    "ecommerce": {
      "transaction_id": "WC_123456",
      "currency": "USD",
      "value": 11239.00,
      "shipping": 499.00,
      "tax": 0.00,
      "coupon": "",
      "items": [
        { "item_id": "1119", "item_name": "75\" Manure Fork Grapple", "price": 4245.00, "quantity": 1, "index": 1 },
        { "item_id": "9359", "item_name": "84\" High Capacity Grapple", "price": 6495.00, "quantity": 1, "index": 2 }
      ]
    },

    "microsoft_ads": {
      "uet_remarketing": {
        "ecomm_pagetype": "purchase",
        "ecomm_prodid": ["1119", "9359"],
        "ecomm_totalvalue": 11239.00,
        "currency": "USD",
        "transaction_id": "WC_123456"
      }
    }
  }
]
