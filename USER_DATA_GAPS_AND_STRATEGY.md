# User Data Lifecycle Gaps and Strategy

## Scope and sources
- Scope: dataLayer user_data handling and lifecycle fields only (ignore HTML/canvas helpers).
- Source: `original-data/messer datalayers new.txt`.

## Observed behavior (source data)
- `user_data` is pushed as an empty array on ecommerce events.
  Evidence: `original-data/messer datalayers new.txt:49`, `original-data/messer datalayers new.txt:144`.
- `user_data` objects are pushed without an `event` key and with `user_id: null`.
  Evidence: `original-data/messer datalayers new.txt:395`.
- `user_init` sets a guest user_id, but that value is not carried into `user_data`.
  Evidence: `original-data/messer datalayers new.txt:207` (guest id), `original-data/messer datalayers new.txt:395` (user_id null).
- Two checkout events exist in the same flow: legacy `checkout` and GA4 `begin_checkout`.
  Evidence: `original-data/messer datalayers new.txt:211`, `original-data/messer datalayers new.txt:242`.
- `user_data` updates appear immediately after field interaction events, indicating PII capture on click/typing instead of validated steps.
  Evidence: `original-data/messer datalayers new.txt:360` (gtm.click), `original-data/messer datalayers new.txt:395` (user_data).

## Gap analysis
1) **user_data clearing and format**
   - Gap: `user_data: []` clears the object, breaking GTM variables that read `user_data.*`.
2) **No event-based user_data updates**
   - Gap: user_data updates are pushed without an `event`, so tags cannot reliably read the latest values.
3) **Identity continuity**
   - Gap: guest `user_id` exists in `user_init`, but `user_data.user_id` is null during checkout updates.
4) **Duplicate checkout event schemas**
   - Gap: two checkout events with different schemas increase double-trigger risk and inconsistent data mapping.
5) **PII timing**
   - Gap: user_data is captured on click/typing rather than validated blur or step completion.
6) **Lifecycle fields missing**
   - Gap: no lifecycle attributes (signup_date, customer_type, last_purchase_date, lifetime_value, etc.) appear in user_data.

## Strategy (user_data + lifecycle)

### Core rule (dataLayer)
- Never push `user_data: []`.
- Always push `user_data` inside an event (ex: `user_data_update`) so GTM can read it reliably.
- Push `user_data_update` before ecommerce events on the same page whenever possible.

### Identity model (best practice)
- `user_id`: stable internal ID for logged-in customers only.
- `guest_id`: first-party random ID for anonymous visitors.
- `external_id`: optional CRM/ERP ID for logged-in users.
- If you need one always-present key, use `identity_id = user_id || guest_id` (keep `user_id` separate for platforms that treat it as authenticated).

### Decision defaults (to remove ambiguity)
- Canonical checkout event should be `begin_checkout`. If a custom `checkout` event remains, it must be renamed or removed to avoid duplicates.
- `user_id` is logged-in only. Guests should use `guest_id`, and `identity_id` should be set to `guest_id`.
- Only send PII (email, phone) after consent. If consent is denied, omit PII fields entirely.

### Lifecycle attributes (what to track)
- `has_account` (boolean) and `signup_date` (ISO date) for signed up users.
- `customer_type`: `new` or `returning` (based on order history, not sessions).
- `first_visit_date`, `last_visit_date` (from cookie/server; update `last_visit_date` each session).
- `last_purchase_date`, `last_purchase_value`, `last_purchase_id` (from WooCommerce order history).
- `purchase_count`, `lifetime_value` (server-computed, numeric, with `currency`).

### Field definitions and update rules
- `first_visit_date`: set once, never overwritten.
- `last_visit_date`: update once per new session; if you need "previous visit", copy the old value before overwriting.
- `customer_type`: evaluate from completed order history prior to the current order.
- `last_purchase_*`: update only when an order reaches the final "completed" state.
- `purchase_count` and `lifetime_value`: aggregate only completed orders; keep numeric types.

### When to push `user_data_update`
- On page load after consent (pre-GTM if possible).
- After login or signup (account state changes).
- After checkout step completion (validated, not on keystroke).
- After purchase confirmation (update last_purchase_*, purchase_count, lifetime_value).
- Only when values change (avoid pushing on every keystroke or click).

### Consent and PII handling
- If consent is denied, omit PII fields instead of sending empty strings.
- Hashing should happen only after consent and only for downstream platforms that require it.

### Data sources and authority
- Logged-in lifecycle fields should come from server-side WooCommerce order history (source of truth).
- Guest fields (guest_id, visit dates) can be client-managed but should be treated as best-effort.

### WooCommerce responsibilities
- Compute lifecycle fields server-side from user meta + order history:
  - customer_type, purchase_count, lifetime_value, last_purchase_*.
- Inject user context into the page (or via an authenticated JSON endpoint) after consent.
- Create and persist `guest_id` + `first_visit_date`/`last_visit_date` (cookie/localStorage).

### GTM responsibilities
- Trigger `user_data_update` and map fields into:
  - GA4 `user_id` + `user_properties` (ex: customer_type, lifetime_value, purchase_count).
  - sGTM/Meta/Ads `user_data` (hashed email/phone only after consent).
- Ensure tags read the latest `user_data` object (event-based, not a global []).

### Example dataLayer push
```js
dataLayer.push({
  event: "user_data_update",
  user_data: {
    user_id: "12345",            // logged-in only
    guest_id: "g_9f3c8b1a",
    identity_id: "12345",
    has_account: true,
    signup_date: "2024-12-20",
    customer_type: "returning",
    first_visit_date: "2024-10-01",
    last_visit_date: "2025-12-29",
    last_purchase_date: "2025-11-03",
    last_purchase_value: 4245.00,
    last_purchase_id: "16506",
    purchase_count: 4,
    lifetime_value: 10740.00,
    currency: "USD"
  }
});
```

### Notes on "previous date visited"
- Store `last_visit_date` before updating it for the current session, or you will overwrite the previous value.
- If you rely on client storage, treat it as best-effort; server-side is authoritative for logged-in users.

## Implementation tasks by owner

### WooCommerce (site/dataLayer)
- Remove all `user_data: []` pushes.
- Decide whether the custom `checkout` event is deleted or renamed to avoid duplicating `begin_checkout`.
- Add lifecycle fields to `user_data` for logged-in users (from order history).
- Persist `guest_id`, `first_visit_date`, `last_visit_date` for anonymous users.
- Push `user_data_update` only after consent and validated field completion.

### GTM (wGTM/sGTM)
- Listen for `user_data_update` and map to GA4 user_id + user_properties.
- Map lifecycle fields into sGTM user data for server-side tags (hash PII only with consent).
- Ensure tags read from the event payload, not stale global objects.

## Validation checklist
- `user_data_update` event exists and contains a non-empty object (no [] payloads).
- `identity_id` is always present; `user_id` is present only for logged-in users.
- `customer_type`, `purchase_count`, `lifetime_value`, and `last_purchase_date` populate for known customers.
- Tags fired after `user_data_update` show the updated values (GA4 user_properties, Meta/Ads user_data).
- No PII is sent before consent, and no `user_id: null` is emitted in user_data updates.
