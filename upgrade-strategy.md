# Enterprise GTM Upgrade Strategy
## Messer Attach - Server-Side Tracking Implementation

> Status: Legacy (2024). Superseded by audit-report.md and GTM_AUDIT_REPORT.md. Current exports show Data Tag uses ce_ecom (Trigger 307) and /metrics routing. Do not apply the implementation steps below unless explicitly requested.

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Current State Analysis](#current-state-analysis)
3. [Enterprise Architecture](#enterprise-architecture)
4. [Data Tag Strategy](#data-tag-strategy)
5. [wGTM Configuration](#wgtm-configuration)
6. [sGTM Configuration](#sgtm-configuration)
7. [Event Routing Matrix](#event-routing-matrix)
8. [Import JSON Templates](#import-json-templates)
9. [Canvas Visualization Approach](#canvas-visualization-approach)
10. [Implementation Checklist](#implementation-checklist)

---

## Executive Summary

### Critical Issue (Legacy Context)
Legacy analysis assumed a single Data Tag firing only on purchase (Trigger 96). Current exports show Data Tag firing on ce_ecom (Trigger 307), so event coverage gaps must be validated with /metrics + sGTM preview rather than inferred from triggers alone.

### Recommended Solution
Implement **multiple Data Tags** grouped by event category, each with specific triggers and data schemas.

---

## Current State Analysis

### What's Working
| Component | Status | Notes |
|-----------|--------|-------|
| WooCommerce DataLayer | ✅ Working | All ecommerce events pushing correctly |
| Consent Mode v2 | ✅ Working | Complianz integration functional |
| CF Worker Proxy | ✅ Working | /gtm/* routing to Stape |
| sGTM Container | ✅ Working | Tags configured but not receiving data |
| gtag.js Path | ✅ Working | /metrics endpoint functional |

### What's Broken (Legacy assumptions)
| Component | Status | Issue |
|-----------|--------|-------|
| Data Tag | ❌ Critical | Legacy claim; current exports show ce_ecom (Trigger 307) |
| Event Coverage | ❌ Critical | ~95% of events never reach sGTM |
| Deduplication | ⚠️ Missing | No client_id/session_id strategy |
| Error Handling | ⚠️ Missing | No fallback for failed requests |

---

## Enterprise Architecture

### Recommended Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              BROWSER (Client-Side)                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────────────────────┐│
│  │ WooCommerce  │────▶│  DataLayer   │────▶│           wGTM               ││
│  │  + Complianz │     │              │     │  ┌─────────────────────────┐ ││
│  └──────────────┘     └──────────────┘     │  │ Data Tags (by category) │ ││
│                                            │  ├─────────────────────────┤ ││
│                                            │  │ • Core Events Tag       │ ││
│                                            │  │ • Ecommerce Tag         │ ││
│                                            │  │ • Engagement Tag        │ ││
│                                            │  │ • Conversion Tag        │ ││
│                                            │  └──────────┬──────────────┘ ││
│                                            └─────────────┼────────────────┘│
└──────────────────────────────────────────────────────────┼─────────────────┘
                                                           │
                                              POST /data   │  (First-Party)
                                                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CF WORKER (Proxy)                              │
│                         messerattach.com/gtm/*                              │
└─────────────────────────────────────────────────────────┬───────────────────┘
                                                          │
                                                          ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              sGTM (Stape.io)                                │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                            CLIENTS                                     │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────┐ │ │
│  │  │  GA4 Client     │  │  Data Client    │  │  Custom Client (opt)    │ │ │
│  │  │  (gtag.js)      │  │  (Data Tags)    │  │  (webhooks, etc)        │ │ │
│  │  └────────┬────────┘  └────────┬────────┘  └────────────┬────────────┘ │ │
│  └───────────┼────────────────────┼────────────────────────┼──────────────┘ │
│              │                    │                        │                │
│              ▼                    ▼                        ▼                │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                           TRIGGERS                                     │ │
│  │  • All Events         • Ecommerce Events    • Page Views               │ │
│  │  • Purchase Only      • Form Submissions    • Custom Events            │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│              │                    │                        │                │
│              ▼                    ▼                        ▼                │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                            TAGS                                        │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │ │
│  │  │   GA4    │  │ Meta CAPI│  │ Gads     │  │ MS UET   │  │ Custom   │  │ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Data Tag Strategy

### Option A: Single Data Tag (Simple)
**NOT RECOMMENDED for enterprise**

```
┌─────────────────────────────────────────┐
│           Single Data Tag               │
│  Trigger: All Events (Custom Event .*)  │
│  Sends: Everything to sGTM              │
└─────────────────────────────────────────┘
```

**Pros:** Simple, one tag to manage
**Cons:** No granular control, debugging nightmare, can't customize payloads per event type

---

### Option B: Multiple Data Tags by Category (RECOMMENDED)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        DATA TAG ARCHITECTURE                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  DATA TAG: Core Events                                              │   │
│  │  ─────────────────────────────────────────────────────────────────  │   │
│  │  Triggers:                                                          │   │
│  │    • page_view                                                      │   │
│  │    • scroll (25%, 50%, 75%, 90%)                                    │   │
│  │    • click (outbound links)                                         │   │
│  │    • file_download                                                  │   │
│  │    • video_start, video_progress, video_complete                    │   │
│  │                                                                     │   │
│  │  Data Sent:                                                         │   │
│  │    • page_location, page_title, page_referrer                       │   │
│  │    • user_id, client_id, session_id                                 │   │
│  │    • consent_state                                                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  DATA TAG: Ecommerce Events                                         │   │
│  │  ─────────────────────────────────────────────────────────────────  │   │
│  │  Triggers:                                                          │   │
│  │    • view_item, view_item_list                                      │   │
│  │    • select_item                                                    │   │
│  │    • add_to_cart, remove_from_cart                                  │   │
│  │    • view_cart                                                      │   │
│  │    • begin_checkout                                                 │   │
│  │    • add_payment_info, add_shipping_info                            │   │
│  │                                                                     │   │
│  │  Data Sent:                                                         │   │
│  │    • items[] (full product array)                                   │   │
│  │    • currency, value                                                │   │
│  │    • item_list_name, item_list_id                                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  DATA TAG: Conversion Events                                        │   │
│  │  ─────────────────────────────────────────────────────────────────  │   │
│  │  Triggers:                                                          │   │
│  │    • purchase                                                       │   │
│  │    • refund                                                         │   │
│  │    • generate_lead                                                  │   │
│  │    • sign_up                                                        │   │
│  │                                                                     │   │
│  │  Data Sent:                                                         │   │
│  │    • transaction_id (CRITICAL for dedup)                            │   │
│  │    • items[], value, currency                                       │   │
│  │    • tax, shipping                                                  │   │
│  │    • coupon                                                         │   │
│  │    • new_customer (boolean)                                         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  DATA TAG: Engagement Events                                        │   │
│  │  ─────────────────────────────────────────────────────────────────  │   │
│  │  Triggers:                                                          │   │
│  │    • form_submit                                                    │   │
│  │    • newsletter_signup                                              │   │
│  │    • contact_click (phone, email)                                   │   │
│  │    • social_share                                                   │   │
│  │    • search                                                         │   │
│  │                                                                     │   │
│  │  Data Sent:                                                         │   │
│  │    • form_id, form_name                                             │   │
│  │    • search_term                                                    │   │
│  │    • engagement_type                                                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Why Multiple Data Tags?

| Benefit | Description |
|---------|-------------|
| **Debugging** | Easily disable one category without affecting others |
| **Performance** | Send only relevant data per event type |
| **Payload Size** | Smaller, optimized payloads |
| **Consent** | Different consent requirements per category |
| **Versioning** | Update ecommerce schema without touching core events |
| **Monitoring** | Track success rates per category |

---

## wGTM Configuration

### Required Variables

```javascript
// ═══════════════════════════════════════════════════════════════════════════
// CONSTANT VARIABLES
// ═══════════════════════════════════════════════════════════════════════════

// CV - Measurement ID
Name: "CV - GA4 Measurement ID"
Type: Constant
Value: "G-XXXXXXXXXX"

// CV - sGTM Endpoint
Name: "CV - sGTM Endpoint"
Type: Constant
Value: "https://messerattach.com/metrics"

// CV - Data Endpoint
Name: "CV - Data Endpoint"
Type: Constant
Value: "https://messerattach.com/metrics/data"

// ═══════════════════════════════════════════════════════════════════════════
// DATA LAYER VARIABLES
// ═══════════════════════════════════════════════════════════════════════════

// DLV - Event Name
Name: "DLV - event"
Type: Data Layer Variable
Data Layer Variable Name: "event"

// DLV - Ecommerce Object
Name: "DLV - ecommerce"
Type: Data Layer Variable
Data Layer Variable Name: "ecommerce"

// DLV - Ecommerce Items
Name: "DLV - ecommerce.items"
Type: Data Layer Variable
Data Layer Variable Name: "ecommerce.items"

// DLV - Ecommerce Value
Name: "DLV - ecommerce.value"
Type: Data Layer Variable
Data Layer Variable Name: "ecommerce.value"

// DLV - Ecommerce Currency
Name: "DLV - ecommerce.currency"
Type: Data Layer Variable
Data Layer Variable Name: "ecommerce.currency"

// DLV - Transaction ID
Name: "DLV - ecommerce.transaction_id"
Type: Data Layer Variable
Data Layer Variable Name: "ecommerce.transaction_id"

// ═══════════════════════════════════════════════════════════════════════════
// CUSTOM JAVASCRIPT VARIABLES
// ═══════════════════════════════════════════════════════════════════════════

// CJS - Client ID
Name: "CJS - Client ID"
Type: Custom JavaScript
function() {
  try {
    var match = document.cookie.match(/_ga=GA\d+\.\d+\.(\d+\.\d+)/);
    return match ? match[1] : undefined;
  } catch(e) {
    return undefined;
  }
}

// CJS - Session ID
Name: "CJS - Session ID"
Type: Custom JavaScript
function() {
  try {
    var match = document.cookie.match(/_ga_[A-Z0-9]+=GS\d+\.\d+\.(\d+)/);
    return match ? match[1] : undefined;
  } catch(e) {
    return undefined;
  }
}

// CJS - User ID (if logged in)
Name: "CJS - User ID"
Type: Custom JavaScript
function() {
  return window.dataLayer && window.dataLayer.find(function(obj) {
    return obj.user_id;
  })?.user_id || undefined;
}

// CJS - Consent State
Name: "CJS - Consent State"
Type: Custom JavaScript
function() {
  return {
    ad_storage: {{Consent State - ad_storage}} || 'denied',
    analytics_storage: {{Consent State - analytics_storage}} || 'denied',
    ad_user_data: {{Consent State - ad_user_data}} || 'denied',
    ad_personalization: {{Consent State - ad_personalization}} || 'denied'
  };
}

// CJS - Is Ecommerce Event
Name: "CJS - Is Ecommerce Event"
Type: Custom JavaScript
function() {
  var ecommerceEvents = [
    'view_item', 'view_item_list', 'select_item',
    'add_to_cart', 'remove_from_cart', 'view_cart',
    'begin_checkout', 'add_payment_info', 'add_shipping_info',
    'purchase', 'refund'
  ];
  return ecommerceEvents.indexOf({{DLV - event}}) > -1;
}
```

### Required Triggers

```javascript
// ═══════════════════════════════════════════════════════════════════════════
// CORE EVENT TRIGGERS
// ═══════════════════════════════════════════════════════════════════════════

// TR - Page View
Name: "TR - Page View"
Type: Page View
Fires on: All Pages

// TR - All Custom Events
Name: "TR - All Custom Events"
Type: Custom Event
Event name: .*
Use regex matching: true

// ═══════════════════════════════════════════════════════════════════════════
// ECOMMERCE TRIGGERS
// ═══════════════════════════════════════════════════════════════════════════

// TR - Ecommerce - View Item
Name: "TR - Ecommerce - View Item"
Type: Custom Event
Event name: view_item|view_item_list|select_item
Use regex matching: true

// TR - Ecommerce - Cart Actions
Name: "TR - Ecommerce - Cart Actions"
Type: Custom Event
Event name: add_to_cart|remove_from_cart|view_cart
Use regex matching: true

// TR - Ecommerce - Checkout
Name: "TR - Ecommerce - Checkout"
Type: Custom Event
Event name: begin_checkout|add_payment_info|add_shipping_info
Use regex matching: true

// TR - Ecommerce - Purchase
Name: "TR - Ecommerce - Purchase"
Type: Custom Event
Event name: purchase

// TR - Ecommerce - All (Combined)
Name: "TR - Ecommerce - All Events"
Type: Trigger Group
Contains:
  - TR - Ecommerce - View Item
  - TR - Ecommerce - Cart Actions
  - TR - Ecommerce - Checkout
  - TR - Ecommerce - Purchase

// ═══════════════════════════════════════════════════════════════════════════
// ENGAGEMENT TRIGGERS
// ═══════════════════════════════════════════════════════════════════════════

// TR - Engagement - Form Submit
Name: "TR - Engagement - Form Submit"
Type: Custom Event
Event name: form_submit|generate_lead|sign_up
Use regex matching: true

// TR - Engagement - Scroll
Name: "TR - Engagement - Scroll"
Type: Scroll Depth
Vertical Scroll Depths: 25, 50, 75, 90

// TR - Engagement - Video
Name: "TR - Engagement - Video"
Type: YouTube Video
Capture: Start, Progress (25%, 50%, 75%), Complete
```

### Required Tags

```javascript
// ═══════════════════════════════════════════════════════════════════════════
// DATA TAG: CORE EVENTS
// ═══════════════════════════════════════════════════════════════════════════

Name: "sGTM - Data Tag - Core Events"
Type: Google Tag: Data Tag
Destination ID: Use lookup table or {{CV - Data Endpoint}}

Event Name: {{DLV - event}}
Event Parameters:
  - page_location: {{Page URL}}
  - page_title: {{Page Title}}
  - page_referrer: {{Referrer}}
  - client_id: {{CJS - Client ID}}
  - session_id: {{CJS - Session ID}}
  - user_id: {{CJS - User ID}}
  - consent_state: {{CJS - Consent State}}
  - timestamp: {{CJS - Timestamp}}

Triggers:
  - TR - Page View
  - TR - Engagement - Scroll
  - TR - Engagement - Video

// ═══════════════════════════════════════════════════════════════════════════
// DATA TAG: ECOMMERCE EVENTS
// ═══════════════════════════════════════════════════════════════════════════

Name: "sGTM - Data Tag - Ecommerce"
Type: Google Tag: Data Tag

Event Name: {{DLV - event}}
Event Parameters:
  - page_location: {{Page URL}}
  - client_id: {{CJS - Client ID}}
  - session_id: {{CJS - Session ID}}
  - user_id: {{CJS - User ID}}
  - currency: {{DLV - ecommerce.currency}}
  - value: {{DLV - ecommerce.value}}
  - items: {{DLV - ecommerce.items}}

Triggers:
  - TR - Ecommerce - View Item
  - TR - Ecommerce - Cart Actions
  - TR - Ecommerce - Checkout

// ═══════════════════════════════════════════════════════════════════════════
// DATA TAG: CONVERSION EVENTS
// ═══════════════════════════════════════════════════════════════════════════

Name: "sGTM - Data Tag - Conversions"
Type: Google Tag: Data Tag

Event Name: {{DLV - event}}
Event Parameters:
  - page_location: {{Page URL}}
  - client_id: {{CJS - Client ID}}
  - session_id: {{CJS - Session ID}}
  - user_id: {{CJS - User ID}}
  - transaction_id: {{DLV - ecommerce.transaction_id}}
  - currency: {{DLV - ecommerce.currency}}
  - value: {{DLV - ecommerce.value}}
  - items: {{DLV - ecommerce.items}}
  - tax: {{DLV - ecommerce.tax}}
  - shipping: {{DLV - ecommerce.shipping}}
  - coupon: {{DLV - ecommerce.coupon}}

Triggers:
  - TR - Ecommerce - Purchase

// ═══════════════════════════════════════════════════════════════════════════
// DATA TAG: ENGAGEMENT EVENTS
// ═══════════════════════════════════════════════════════════════════════════

Name: "sGTM - Data Tag - Engagement"
Type: Google Tag: Data Tag

Event Name: {{DLV - event}}
Event Parameters:
  - page_location: {{Page URL}}
  - client_id: {{CJS - Client ID}}
  - form_id: {{DLV - form_id}}
  - form_name: {{DLV - form_name}}
  - search_term: {{DLV - search_term}}

Triggers:
  - TR - Engagement - Form Submit
```

---

## sGTM Configuration

### Required Clients

```javascript
// ═══════════════════════════════════════════════════════════════════════════
// CLIENT: GA4 (for gtag.js requests)
// ═══════════════════════════════════════════════════════════════════════════

Name: "GA4 Client"
Type: GA4
Priority: 1
Default GA4 paths: Enabled
Claim requests: Yes

// ═══════════════════════════════════════════════════════════════════════════
// CLIENT: Data Client (for Data Tag requests)
// ═══════════════════════════════════════════════════════════════════════════

Name: "Data Client"
Type: Data Tag
Priority: 2
Request path: /data
Claim requests: Yes
```

### Required Triggers

```javascript
// ═══════════════════════════════════════════════════════════════════════════
// sGTM TRIGGERS
// ═══════════════════════════════════════════════════════════════════════════

// TR - All Events (Data Client)
Name: "TR - All Events - Data Client"
Type: Custom
Condition: Client Name equals "Data Client"

// TR - GA4 Events
Name: "TR - GA4 Events"
Type: Custom
Condition: Client Name equals "GA4"

// TR - Ecommerce Events
Name: "TR - Ecommerce Events"
Type: Custom
Conditions:
  - Client Name equals "Data Client"
  - Event Name matches RegEx: view_item|add_to_cart|begin_checkout|purchase

// TR - Purchase Only
Name: "TR - Purchase Only"
Type: Custom
Conditions:
  - Client Name equals "Data Client"
  - Event Name equals "purchase"

// TR - Page View Only
Name: "TR - Page View Only"
Type: Custom
Conditions:
  - Client Name equals "Data Client"
  - Event Name equals "page_view"
```

### Required Tags

```javascript
// ═══════════════════════════════════════════════════════════════════════════
// sGTM TAG: GA4
// ═══════════════════════════════════════════════════════════════════════════

Name: "GA4 - All Events"
Type: GA4
Measurement ID: G-XXXXXXXXXX
Event Name: {{Event Name}}
Send to: Google Analytics

Event Parameters (from Event Data):
  - All parameters auto-forwarded

User Properties:
  - user_id: {{Event Data - user_id}}
  - client_id: {{Event Data - client_id}}

Triggers:
  - TR - All Events - Data Client
  - TR - GA4 Events

// ═══════════════════════════════════════════════════════════════════════════
// sGTM TAG: Meta Conversions API
// ═══════════════════════════════════════════════════════════════════════════

Name: "Meta CAPI - All Events"
Type: Meta Conversions API
Pixel ID: XXXXXXXXXX
Access Token: {{CV - Meta Access Token}}

Event Name: {{Event Name}}
Event ID: {{Event Data - event_id}} // For deduplication

User Data:
  - email: {{Event Data - user_email}}
  - phone: {{Event Data - user_phone}}
  - external_id: {{Event Data - user_id}}
  - client_ip_address: {{Client IP}}
  - client_user_agent: {{User Agent}}
  - fbc: {{Event Data - fbc}}
  - fbp: {{Event Data - fbp}}

Custom Data:
  - currency: {{Event Data - currency}}
  - value: {{Event Data - value}}
  - content_ids: {{Event Data - item_ids}}
  - contents: {{Event Data - items}}

Triggers:
  - TR - Ecommerce Events

// ═══════════════════════════════════════════════════════════════════════════
// sGTM TAG: Google Ads Conversions
// ═══════════════════════════════════════════════════════════════════════════

Name: "Google Ads - Purchase"
Type: Google Ads Conversion Tracking
Conversion ID: AW-XXXXXXXXXX
Conversion Label: XXXXXXXXXX

Conversion Value: {{Event Data - value}}
Currency: {{Event Data - currency}}
Transaction ID: {{Event Data - transaction_id}}
New Customer: {{Event Data - new_customer}}

Enhanced Conversions:
  - email: {{Event Data - user_email}}
  - phone: {{Event Data - user_phone}}
  - first_name: {{Event Data - first_name}}
  - last_name: {{Event Data - last_name}}
  - address: {{Event Data - address}}

Triggers:
  - TR - Purchase Only

// ═══════════════════════════════════════════════════════════════════════════
// sGTM TAG: Microsoft UET
// ═══════════════════════════════════════════════════════════════════════════

Name: "Microsoft UET - All Events"
Type: Microsoft UET
Tag ID: XXXXXXXXXX

Event Action: {{Event Name}}
Event Category: ecommerce
Event Label: {{Event Data - item_name}}
Event Value: {{Event Data - value}}
Currency: {{Event Data - currency}}

Triggers:
  - TR - All Events - Data Client
```

---

## Event Routing Matrix

### Which Events Go Where?

| Event | GA4 | Meta CAPI | Google Ads | MS UET | Pinterest | TikTok |
|-------|-----|-----------|------------|--------|-----------|--------|
| page_view | ✅ | ✅ PageView | ❌ | ✅ | ✅ | ✅ |
| view_item | ✅ | ✅ ViewContent | ❌ | ✅ | ✅ | ✅ |
| view_item_list | ✅ | ✅ ViewContent | ❌ | ✅ | ✅ | ✅ |
| add_to_cart | ✅ | ✅ AddToCart | ❌ | ✅ | ✅ | ✅ |
| view_cart | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| begin_checkout | ✅ | ✅ InitiateCheckout | ❌ | ✅ | ✅ | ✅ |
| add_payment_info | ✅ | ✅ AddPaymentInfo | ❌ | ❌ | ❌ | ❌ |
| purchase | ✅ | ✅ Purchase | ✅ | ✅ | ✅ | ✅ |
| generate_lead | ✅ | ✅ Lead | ✅ | ✅ | ✅ | ✅ |
| sign_up | ✅ | ✅ CompleteRegistration | ❌ | ❌ | ❌ | ✅ |

### Event Name Mapping

```javascript
// sGTM Variable: Event Name Mapper
function() {
  var eventMap = {
    // GA4 Name → Platform-specific name
    'page_view': {
      'meta': 'PageView',
      'pinterest': 'pagevisit',
      'tiktok': 'PageView'
    },
    'view_item': {
      'meta': 'ViewContent',
      'pinterest': 'pagevisit',
      'tiktok': 'ViewContent'
    },
    'add_to_cart': {
      'meta': 'AddToCart',
      'pinterest': 'addtocart',
      'tiktok': 'AddToCart'
    },
    'begin_checkout': {
      'meta': 'InitiateCheckout',
      'pinterest': 'checkout',
      'tiktok': 'InitiateCheckout'
    },
    'purchase': {
      'meta': 'Purchase',
      'pinterest': 'checkout',
      'tiktok': 'CompletePayment'
    }
  };

  var ga4Event = {{Event Name}};
  var platform = {{Lookup - Current Tag Platform}};

  return eventMap[ga4Event]?.[platform] || ga4Event;
}
```

---

## Import JSON Templates

### wGTM Container Import (Partial)

Save as `wgtm-data-tags-import.json`:

```json
{
  "exportFormatVersion": 2,
  "containerVersion": {
    "tag": [
      {
        "name": "sGTM - Data Tag - Core Events",
        "type": "googtag",
        "parameter": [
          {
            "type": "TEMPLATE",
            "key": "tagId",
            "value": "{{CV - Data Endpoint}}"
          },
          {
            "type": "TEMPLATE",
            "key": "eventName",
            "value": "{{DLV - event}}"
          }
        ],
        "firingTriggerId": ["TR_PAGE_VIEW", "TR_SCROLL", "TR_VIDEO"],
        "tagFiringOption": "ONCE_PER_EVENT"
      },
      {
        "name": "sGTM - Data Tag - Ecommerce",
        "type": "googtag",
        "parameter": [
          {
            "type": "TEMPLATE",
            "key": "tagId",
            "value": "{{CV - Data Endpoint}}"
          },
          {
            "type": "TEMPLATE",
            "key": "eventName",
            "value": "{{DLV - event}}"
          },
          {
            "type": "LIST",
            "key": "eventParameters",
            "list": [
              {
                "type": "MAP",
                "map": [
                  {"type": "TEMPLATE", "key": "name", "value": "items"},
                  {"type": "TEMPLATE", "key": "value", "value": "{{DLV - ecommerce.items}}"}
                ]
              },
              {
                "type": "MAP",
                "map": [
                  {"type": "TEMPLATE", "key": "name", "value": "value"},
                  {"type": "TEMPLATE", "key": "value", "value": "{{DLV - ecommerce.value}}"}
                ]
              },
              {
                "type": "MAP",
                "map": [
                  {"type": "TEMPLATE", "key": "name", "value": "currency"},
                  {"type": "TEMPLATE", "key": "value", "value": "{{DLV - ecommerce.currency}}"}
                ]
              }
            ]
          }
        ],
        "firingTriggerId": ["TR_ECOMMERCE_ALL"],
        "tagFiringOption": "ONCE_PER_EVENT"
      },
      {
        "name": "sGTM - Data Tag - Conversions",
        "type": "googtag",
        "parameter": [
          {
            "type": "TEMPLATE",
            "key": "tagId",
            "value": "{{CV - Data Endpoint}}"
          },
          {
            "type": "TEMPLATE",
            "key": "eventName",
            "value": "{{DLV - event}}"
          },
          {
            "type": "LIST",
            "key": "eventParameters",
            "list": [
              {
                "type": "MAP",
                "map": [
                  {"type": "TEMPLATE", "key": "name", "value": "transaction_id"},
                  {"type": "TEMPLATE", "key": "value", "value": "{{DLV - ecommerce.transaction_id}}"}
                ]
              },
              {
                "type": "MAP",
                "map": [
                  {"type": "TEMPLATE", "key": "name", "value": "items"},
                  {"type": "TEMPLATE", "key": "value", "value": "{{DLV - ecommerce.items}}"}
                ]
              },
              {
                "type": "MAP",
                "map": [
                  {"type": "TEMPLATE", "key": "name", "value": "value"},
                  {"type": "TEMPLATE", "key": "value", "value": "{{DLV - ecommerce.value}}"}
                ]
              }
            ]
          }
        ],
        "firingTriggerId": ["TR_PURCHASE"],
        "tagFiringOption": "ONCE_PER_EVENT"
      }
    ],
    "trigger": [
      {
        "name": "TR - Ecommerce - All Events",
        "type": "CUSTOM_EVENT",
        "customEventFilter": [
          {
            "type": "MATCH_REGEX",
            "parameter": [
              {"type": "TEMPLATE", "key": "arg0", "value": "{{_event}}"},
              {"type": "TEMPLATE", "key": "arg1", "value": "^(view_item|view_item_list|select_item|add_to_cart|remove_from_cart|view_cart|begin_checkout|add_payment_info|add_shipping_info)$"}
            ]
          }
        ]
      },
      {
        "name": "TR - Purchase",
        "type": "CUSTOM_EVENT",
        "customEventFilter": [
          {
            "type": "EQUALS",
            "parameter": [
              {"type": "TEMPLATE", "key": "arg0", "value": "{{_event}}"},
              {"type": "TEMPLATE", "key": "arg1", "value": "purchase"}
            ]
          }
        ]
      }
    ],
    "variable": [
      {
        "name": "DLV - ecommerce.items",
        "type": "v",
        "parameter": [
          {"type": "INTEGER", "key": "dataLayerVersion", "value": "2"},
          {"type": "TEMPLATE", "key": "name", "value": "ecommerce.items"}
        ]
      },
      {
        "name": "DLV - ecommerce.value",
        "type": "v",
        "parameter": [
          {"type": "INTEGER", "key": "dataLayerVersion", "value": "2"},
          {"type": "TEMPLATE", "key": "name", "value": "ecommerce.value"}
        ]
      },
      {
        "name": "DLV - ecommerce.currency",
        "type": "v",
        "parameter": [
          {"type": "INTEGER", "key": "dataLayerVersion", "value": "2"},
          {"type": "TEMPLATE", "key": "name", "value": "ecommerce.currency"}
        ]
      },
      {
        "name": "DLV - ecommerce.transaction_id",
        "type": "v",
        "parameter": [
          {"type": "INTEGER", "key": "dataLayerVersion", "value": "2"},
          {"type": "TEMPLATE", "key": "name", "value": "ecommerce.transaction_id"}
        ]
      }
    ]
  }
}
```

### How to Import

1. **wGTM Import:**
   - Go to GTM → Admin → Import Container
   - Choose file: `wgtm-data-tags-import.json`
   - Select "Merge" → "Rename conflicting"
   - Review and confirm

2. **sGTM Import:**
   - Similar process for server container
   - Import clients, triggers, and tags separately if needed

---

## Canvas Visualization Approach

### Option 1: Toggle View (Recommended)

Add a **"Strategy View"** toggle button that switches between:
- **Current State** - Shows actual broken implementation
- **Target State** - Shows recommended enterprise architecture

```javascript
// Add to canvas.html
const [viewMode, setViewMode] = useState('current'); // 'current' | 'target'

// Different node/edge sets per mode
const nodes = viewMode === 'current' ? currentNodes : targetNodes;
const edges = viewMode === 'current' ? currentEdges : targetEdges;
```

### Option 2: Expandable Strategy Sections

Add collapsible sections to existing nodes showing:
- Current config (red if broken)
- Recommended config (green)

```javascript
// Inside wGTM node
{
  title: 'Data Tags',
  items: [
    { text: 'Current: 1 tag (ce_ecom trigger)', type: 'error' },
    { text: 'Recommended: 4 tags by category', type: 'success' }
  ]
}
```

### Option 3: Overlay Layer

Add a semi-transparent overlay showing recommended additions:
- Dashed lines for missing connections
- Ghost nodes for missing components
- Annotations explaining changes needed

### Recommended Canvas Changes

```
┌─────────────────────────────────────────────────────────────────┐
│                        TOOLBAR ADDITIONS                        │
├─────────────────────────────────────────────────────────────────┤
│  [Select] [Hand] [Fit] │ View: [Current ▼] │ [Export Strategy] │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     wGTM NODE EXPANSION                         │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ DATA TAGS                                                │   │
│  │ ┌─────────────────────────────────────────────────────┐ │   │
│  │ │ ⚠️ Current (Broken)                                 │ │   │
│  │ │   • Data Tag → Trigger 307 (ce_ecom)          │ │   │
│  │ └─────────────────────────────────────────────────────┘ │   │
│  │ ┌─────────────────────────────────────────────────────┐ │   │
│  │ │ ✅ Recommended                                      │ │   │
│  │ │   • Core Events Tag → page_view, scroll, video     │ │   │
│  │ │   • Ecommerce Tag → view_item, add_to_cart, etc    │ │   │
│  │ │   • Conversion Tag → purchase, refund              │ │   │
│  │ │   • Engagement Tag → form_submit, search           │ │   │
│  │ └─────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Implementation Checklist

### Phase 1: Foundation (Critical)

- [ ] **Fix Data Tag Trigger**
  - Confirm Data Tag uses Trigger 307 (ce_ecom)
  - Or create multiple Data Tags per category

- [ ] **Add Missing Variables**
  - [ ] DLV - ecommerce.items
  - [ ] DLV - ecommerce.value
  - [ ] DLV - ecommerce.currency
  - [ ] DLV - ecommerce.transaction_id
  - [ ] CJS - Client ID
  - [ ] CJS - Session ID

- [ ] **Add Missing Triggers**
  - [ ] TR - Ecommerce - View Item
  - [ ] TR - Ecommerce - Cart Actions
  - [ ] TR - Ecommerce - Checkout
  - [ ] TR - Page View

### Phase 2: Data Tags

- [ ] **Create Core Events Data Tag**
  - Trigger: page_view, scroll, video events
  - Data: page info, client/session IDs

- [ ] **Create Ecommerce Data Tag**
  - Trigger: view_item, add_to_cart, begin_checkout
  - Data: items[], value, currency

- [ ] **Create Conversion Data Tag**
  - Trigger: purchase
  - Data: transaction_id, items[], value, tax, shipping

- [ ] **Create Engagement Data Tag**
  - Trigger: form_submit, search
  - Data: form details, search terms

### Phase 3: sGTM Tags

- [ ] **Verify GA4 Tag**
  - Receiving all events from Data Client
  - User properties mapped correctly

- [ ] **Configure Meta CAPI**
  - Event mapping (GA4 → Meta events)
  - User data enrichment
  - Deduplication via event_id

- [ ] **Configure Google Ads**
  - Enhanced conversions setup
  - Transaction ID for dedup

- [ ] **Configure Microsoft UET**
  - Event mapping
  - Revenue tracking

### Phase 4: Testing & QA

- [ ] **Test Each Event Type**
  - page_view in GA4 Real-Time
  - view_item in GA4 Real-Time
  - add_to_cart in GA4 Real-Time
  - purchase in GA4 Real-Time

- [ ] **Verify sGTM Reception**
  - Check Stape logs
  - Verify all events arriving
  - Check payload completeness

- [ ] **Platform Verification**
  - Meta Events Manager
  - Google Ads Conversion tracking
  - Microsoft UET Tag Helper

### Phase 5: Monitoring

- [ ] **Set Up Alerts**
  - Event volume drop alerts
  - Error rate monitoring
  - Latency tracking

- [ ] **Documentation**
  - Update architecture diagrams
  - Create runbooks
  - Document variable naming conventions

---

## Additional Considerations

### Deduplication Strategy

```javascript
// Generate unique event_id for deduplication
// In wGTM, create a Custom JavaScript variable:

function() {
  var timestamp = Date.now();
  var random = Math.random().toString(36).substring(2, 9);
  var eventName = {{DLV - event}} || 'unknown';
  return eventName + '_' + timestamp + '_' + random;
}

// This event_id is sent to:
// - Meta CAPI (for browser/server dedup)
// - GA4 (as event parameter)
// - Any other platform supporting dedup
```

### Consent Mode Integration

```javascript
// Ensure tags respect consent
// In sGTM, check consent before firing:

Name: "TR - Has Analytics Consent"
Type: Custom
Condition:
  x-ga-gcs contains "G1" // Analytics consent granted
  OR
  Event Data - consent_state.analytics_storage equals "granted"
```

### Error Handling

```javascript
// In sGTM, create a monitoring tag:

Name: "Monitoring - Log Failures"
Type: HTTP Request
URL: https://your-monitoring-endpoint.com/log
Method: POST
Body: {
  "event": "{{Event Name}}",
  "error": "{{Error Message}}",
  "timestamp": "{{Timestamp}}",
  "client_id": "{{Event Data - client_id}}"
}

Trigger: Tag Failure (built-in trigger)
```

---

## Summary

| Question | Answer |
|----------|--------|
| Single or multiple Data Tags? | **Multiple** - one per event category |
| Why multiple? | Debugging, performance, consent, versioning |
| What's broken now? | Data Tag only fires on purchase |
| What percentage of events lost? | ~95% |
| How to visualize on canvas? | Add toggle view (Current vs Target) |
| How to import? | Use GTM Admin → Import Container |
| What else is needed? | Deduplication, error handling, monitoring |

---

*Document created: December 28, 2024*
*For: Messer Attach Server-Side GTM Implementation*
