# URL policy, canonicals and migrations

Choose one canonical HTTPS origin and explicit policies for hostname, case, trailing slash, parameters, encodings, locale and pagination. Redirect variants directly to final intended URL where feasible, preserving allowed campaign params and meaningful query values. Do not redirect arbitrary missing URLs to home. Use canonical hints for equivalent duplicate URLs; canonicals are not directives or replacements for redirects. Align internal links, sitemap, metadata, structured data and response redirects. Every intended indexable page should have a consistent preferred URL; self-canonical is a useful project policy, not a universal technical requirement.

## Migration runbook

Before: inventory old URLs from crawl, sitemap, logs, backlinks and search exports; map to equivalent new URLs; mark no-replacement URLs 404/410; check domain ownership, certificates, routing, content parity, analytics, robots and capacity. Preserve URLs when a redesign does not require changes. Test staging with access protection. Prepare rollback, backups and owner sign-off.

Deploy: apply permanent server redirects, update internal links and metadata, emit new sitemap, verify search properties and applicable site-move workflow. Test variants and important routes by GET; no loops or avoidable chains. Keep permitted attribution parameters. Do not canonicalize all paginated/filter pages indiscriminately to one page if content differs.

After: monitor status errors, crawl, indexing, canonical selection, query/page performance and leads; distinguish expected volatility from defects. Keep redirects long-term where feasible. Use logs and search reports; do not judge on one day. Document new issue mapping and old URL retirement.

Sources: [canonicalization](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls), [site moves](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes).
