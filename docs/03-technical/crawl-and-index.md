# Crawling, indexing, robots and sitemaps

For scoped discovery, crawler policy, robots retrieval and sitemap/crawl-budget evidence use [T05](t05-crawling-robots.md). Separate crawler permission, observed response, coverage and intended index policy; do not infer actual search-engine crawl budget from an audit limit.

## URL response contract

| URL class | Expected behavior |
|---|---|
| Public canonical | 200, meaningful content, crawlable, no accidental noindex |
| Permanent move | 301/308 to true replacement |
| Temporary move | 302/307 when justified |
| Missing | 404/410; useful error UI, not home redirect |
| Private | Authentication/authorization; robots is not security |
| Intentionally nonindexable | Appropriate noindex or status; crawler must access noindex |
| Server failure | Accurate 5xx; investigate and recover |

Robots.txt governs crawling, not guaranteed removal. `noindex` in HTML or X-Robots-Tag must be visible to crawler. Do not block CSS, JavaScript, images or requests needed for rendering. Test CDN/WAF and auth rules. Staging must be protected (prefer authentication), not merely hidden from navigation.

Generate XML sitemap from the authoritative route/content registry: final canonical absolute URLs only, no redirects/404s/noindex, meaningful lastmod only, XML-escape values. Reference in robots.txt and submit to search platforms. Split large sitemaps per protocol limits when needed. Avoid changing all lastmod on each build. Sitemaps are not a substitute for internal links.

## Validation

Request GET (HEAD may differ); inspect headers, source tags, redirects, robots rules and rendered DOM. Review representative URLs in Google URL Inspection and Bing Live URL/Inspection. Compare submitted, discovered and selected canonical sets. Investigate soft 404s, blocked resources, duplicate selection, HTML fallback and server errors. Crawl only authorized sites with responsible limits. Inspect logs with verified crawler identities; a user agent alone is not proof.

Sources: [technical requirements](https://developers.google.com/search/docs/essentials/technical), [robots](https://developers.google.com/search/docs/crawling-indexing/robots/intro), [sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap), [HTTP status codes](https://developers.google.com/crawling/docs/troubleshooting/http-status-codes).
