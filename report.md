# HAR Analysis Report - messerattach.com.har

## Capture summary
- Source: `temp/messerattach.com.har`
- Entries: 62 (52 script, 5 xhr, 3 fetch, 2 image)
- Page timing: onContentLoad 304 ms, onLoad 791 ms for `https://messerattach.com/product/stump-bucket/`
- Status codes: 200 (58), 204 (4), 0 errors, 0 redirects, all HTTPS

## Findings (potential issues)
1) Duplicate WooCommerce cart fragment refresh calls (~0.82 s each)
   - Evidence: two POSTs to `https://messerattach.com/?wc-ajax=get_refreshed_fragments` at 816-822 ms.
   - Impact: extra backend load and latency on page load; often caused by duplicate fragment scripts or theme/plugin duplication.

2) Slow admin-ajax tracking call (1.03 s)
   - Evidence: POST `https://messerattach.com/wp-admin/admin-ajax.php` (action=platform_tracks, tracksEventName=product_page_view) took 1032 ms.
   - Impact: adds backend work and can block the page if awaited; investigate plugin handling of platform_tracks.

3) GA4 page_view only, no ecommerce events in GA4
   - Evidence: only GA4 hits are two calls to `https://messerattach.com/metrics/mc/collect` with `en=page_view` and no `view_item`, `add_to_cart`, etc.
   - Impact: product page ecommerce tracking likely incomplete.

4) Dual GA4 measurement IDs receiving page_view
   - Evidence: page_view sent to `tid=MC-BB3SVL81ZH` and `tid=MC-29YWYGTL3M`.
   - Impact: duplicate data unless intentionally tracking two GA4 properties.

5) Third-party rates API responses not compressed
   - Evidence: `https://quote.firstcitizensef.com/api/rates` responses (Lease and Loan) return 174 KB and 7.5 KB JSON with no Content-Encoding; Cache-Control is `no-cache`.
   - Impact: extra transfer time; consider gzip/brotli on the API or a compressed proxy.

6) Third-party widget script uncacheable and large
   - Evidence: `https://cdn.directcapital.com/scripts/widget.js?v=0.2494529223921521` is 251 KB with no Cache-Control/Expires headers and a random version query param.
   - Impact: forces download on every visit; prefer stable versioning and cache headers.

## Observed tagging/analytics calls
- Microsoft Clarity: `https://o.clarity.ms/collect` (204)
- Bing UET: `https://bat.bing.com/action/0` (204, view_item)
- GA4 via first-party proxy: `https://messerattach.com/metrics/mc/collect` (page_view only)
- GTM server-side plugin JS: `https://messerattach.com/wp-content/plugins/gtm-server-side/assets/js/javascript.js?ver=2.1.41`

## Gaps / capture limitations
- No `document` or `text/html` entries are present in the HAR (resource types are only script/xhr/fetch/image).
- This prevents validating main HTML response headers (CSP, HSTS, cache) and confirming whether the GTM/gtag snippet is present in the base document.
- For a more complete analysis, re-export the HAR with "Preserve log" and ensure the initial document request is captured.
