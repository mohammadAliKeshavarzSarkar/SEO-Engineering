# Troubleshooting playbooks

| Symptom | Investigate in order | Verify fix |
|---|---|---|
| Not indexed | HTTP → robots/WAF → noindex → render → links/sitemap → canonical → quality | live & indexed inspection over time |
| Soft 404 | status and body on missing vs valid routes; generic SPA fallback | true 404, relevant redirects only |
| Google selected other canonical | duplicate variants, conflicting HTML/redirect/link/sitemap, content similarity | consistent final URL and indexed selection |
| Clicks drop | report delay/filter, release annotations, security/manual actions, impressions, pages/devices, CTR vs position, demand | compare matched cohorts after sufficient data |
| Impressions rise, CTR falls | query mix, rankings, titles/snippets, SERP features, device | localized SERP and cohort CTR; avoid universal CTR targets |
| Organic clicks but no leads | event integrity, consent, actual form acceptance, intent/CTA and UX | verified backend outcome, event count and funnel |
| CWV regression | field distribution vs lab; route/device; LCP subparts, long tasks, layout movement | controlled test + post-release field trend |
| Schema invalid | syntax, supported type/properties, visible parity, canonical/asset access | validator, rich results and inspection |
| Crawled but no index | content uniqueness/value, internal links, canonical, status | fix evidence-based cause; avoid repeated submissions |

For traffic drops, segment equations: total clicks ≈ impressions × CTR (aggregate); a change in query mix can alter averages. Compare same weekdays/season, region, device, branded/nonbranded and affected templates. Do not infer penalty from volatility. Check tracking and report lag first; if live eligibility broken, remediate immediately.

For international or CDN discrepancies, inspect representative geo and device requests with authorized tools; distinguish cache keys, locale redirects, WAF and deployment differences. Document actual data vs assumptions. Roll back only when regression evidence and risks justify it.

Sources: [debug Search traffic drops](https://developers.google.com/search/docs/monitor-debug/debugging-search-traffic-drops), [URL inspection](https://support.google.com/webmasters/answer/9012289).

For a full incident procedure, competing hypotheses, bounded evidence records and separate technical/search recovery, use [T12](../03-technical/t12-technical-troubleshooting.md) and [incident workflow](../../workflows/technical-incident.md).
