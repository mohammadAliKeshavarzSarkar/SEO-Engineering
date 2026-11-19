# Search Console, Bing and server evidence

Search Console measures Google search presentation and indexing; Bing Webmaster Tools measures Bing. Analytics measures recorded visits; server/CDN logs measure requests. Do not equate clicks with sessions, crawl with index, or index with ranking. Search Console query data may omit anonymized terms and API outputs may not include all rows.

## Setup and workflow

Verify appropriate properties with least privilege, submit canonical sitemap, inspect sample URLs per template and review indexing, crawl stats, performance, enhancements, security and manual actions. Compare live inspection (current fetch/render) and indexed state (processed view). Search Console URL Inspection live tests are not indexing guarantees. In Bing, inspect redirect targets separately where Live URL behavior requires; use Site Scan for repeatable investigation; warnings are not automatic ranking factors.

Report indexed intended URLs, exclusions by reason, nonbranded and branded impressions/clicks, page and intent clusters, CTR and search appearance. Compare stable periods/devices/markets; average position depends on query and result type. Check Google's [Search Console data anomaly register](https://support.google.com/webmasters/answer/6211453) for the exact report and dates before attributing discontinuities to site changes; distinguish data-logging errors from actual visibility loss. Annotate deployments and search updates. Export query/page reports with dates, dimensions, filters and data limitations; maintain brand regex manually where native reporting is unavailable or unsuitable. Google documents a Generative AI performance report; consult [AI search guidance](../07-specialties/ai-search.md) and current feature/report definitions. Verify API support and actual property eligibility independently. Avoid double-counting overlapping reporting surfaces.

IndexNow: notify participating engines of real added, updated and deleted URLs per current protocol; include preferred URLs and formerly valid deleted/moved URLs as appropriate. Do not submit unchanged pages per build or treat notification as indexation. Keep sitemaps and links.

Server logs: verify bot identities using supported methods, sample URL/status/time/bytes, check errors and wasted variants. Protect logs as potentially sensitive; limit access and retention. Bot requests do not prove use in AI answers.

Sources: [Search Console](https://developers.google.com/search/docs/monitor-debug/search-console-start), [Search Analytics API](https://developers.google.com/webmaster-tools/v1/searchanalytics/query), [Bing URL Inspection](https://www.bing.com/webmasters/help/url-inspection-55a30305), [IndexNow](https://www.indexnow.org/).
