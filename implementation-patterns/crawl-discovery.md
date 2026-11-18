# Crawl discovery and robots implementation patterns

Use [T05](../docs/03-technical/t05-crawling-robots.md). Illustrative synthetic policies only, not deployable defaults. Review actual origin, intended URL inventory and crawler rules, including encoded paths and scope. No network executed.

## A. Narrow policy rather than blanket block
For a fictional catalog with an intentionally non-acquisition filter parameter and needed public assets, a possible rule set for the reviewed generic group is:
```text
User-agent: *
Disallow: /catalog?*sort=
Sitemap: https://example.org/sitemap.xml
```
This example is deliberately narrow and only covers the shown path spelling; it is not a universal filter rule. Check slash variants, query placement, parameter encoding, meaningful routes and crawler-specific groups. Do not add an artificial user-agent group expecting wildcard inheritance. Test using a verified evaluator, not this library's observations checker. If a previously indexed filter URL must be removed, blocking crawl can obstruct directive discovery; review appropriate removal separately. Never list secret paths as security.

## B. Fixture acceptance for a verified evaluator
Synthetic expected results in RFC/Google-compatible path matching with one group:
```text
User-agent: *
Disallow: /articles/
Allow: /articles/public/
Disallow: /archive$
```
| Path | Expected decision for shown group |
|---|---|
| /articles/hidden/ | disallow |
| /articles/public/guide/ | allow |
| /archive | disallow |
| /archive/2026/ | allow |
| /assets/app.js | allow |
Test equal-specificity tie, duplicate groups, case differences, percent encoding and query handling separately against applicable documented policy. Different origin requires different policy. Test retrieval success, 404, 429, 503, redirect boundary and timeout as distinct conditions. Conservative own-provider recovery is not Google's error fallback. Keep actual authorization independent.

## C. Sitemap generation and discovery reconciliation
Use approved registry, select actually published intended representatives, preserve absolute URL and encode XML with trusted serializer. Split by useful cohort within protocol limits. Meaningful lastmod only. Review actual generated/served file and submission scope independently. Example:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://example.org/guide/</loc></url>
</urlset>
```
Map each intended URL to actual status, applicable directives, canonical preference and internal links. Unknown/failed collection is not invalid URL; do not automatically remove it. A sitemap cannot prove site-wide link coverage. Keep old and new inventories for comparison. For runtime frameworks generate through existing route/content owner, validate actual endpoint and cache behavior.

## D. Offline review and actual acceptance
```sh
python3 scripts/audit_crawl_evidence.py --input examples/crawl-evidence/sample.json --output crawl-evidence-report.json
```
No crawl/parser executed. Validate actual robots group/decision and sitemap independently using approved provider, scoped response evidence and rendered resource checks. Test intended row, disallowed utility, required asset, dynamic/query/locale route and blocked/failed retrieval. Set bounded limits; stop on policy uncertainty, auth failure or host strain. Record scope, stop reason, identity/version and reviewed correction, and recheck comparable evidence. See T05 references.
