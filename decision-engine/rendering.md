# Rendering strategy decision protocol

Use for public routes where JavaScript delivery, metadata, deep linking or performance may prevent useful search access. Do not use a framework name alone as evidence.

Before attributing discrepancies to JavaScript, use [T02 paired-observation procedure](../docs/03-technical/t02-javascript-rendering.md). Check comparable request/deployment/profile, complete captures and actual readiness; incomplete/failed renders defer absence claims. Distinguish no-interaction from interaction evidence. Keep HTTP and meta directives separate. Initial applicable noindex remains reviewable independently of the paired comparison.

## Inputs and branch rules

| Observation | Decision / next check |
|---|---|
| Private/authenticated surface | Keep it protected; do not expose via prerender or sitemap |
| Public route has correct source HTML, status, metadata and crawlable links | Retain existing strategy unless a demonstrated performance or reliability need exists |
| Source HTML lacks key content but rendered output is complete | Evaluate bot rendering, indexing evidence, performance, freshness and operational cost. CSR may be acceptable; consider SSG/SSR only with justified benefit |
| Initial response contains unintended noindex but DOM removes it | Fix the initial directive at its actual source and inspect HTTP headers; do not assume Google renders through initial noindex. Preserve deliberate exclusion and authorization. |
| Capture timed out, is incomplete, or context differs | Record failure/unknown; check readiness, logs and matched captures before inferring missing content or regression |
| Rendered output fails or content requires interaction | Diagnose blocked resources, JS/route error, state/interaction dependency. Repair smallest cause; then consider rendering strategy |
| Unknown route serves generic 200 shell | Fix server/edge routing and 404 response independent of rendering framework where possible |
| Few stable marketing/editorial routes | SSG/pre-render is a candidate; test freshness, metadata and deep-link coverage |
| Highly dynamic public data | SSR/hybrid may fit; test cache, correctness, failure states and operational cost |
| No code/hosting or live inspection access | Report unknowns; propose concrete tests and alternatives, not a migration verdict |

Keep canonical policy, route URLs, user-visible content and functionality stable across changes. Do not serve materially different content to search crawlers as an SEO trick.

## Verify and recover

Compare GET status and initial HTML of representative public routes and missing URLs; inspect rendered DOM, navigation/hydration, mobile content and links; validate unique appropriate head metadata and consistency; inspect production and Search Console/Bing as authorized. Compare performance and maintain deployment rollback. If regression appears, revert rendering change or fix affected route without overwriting unrelated work. Indexing may lag; verify processed state separately.

See [rendering guide](../docs/03-technical/rendering-and-architecture.md) and [Google JavaScript SEO](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics); check current source before production changes.

Use [route delivery](../implementation-patterns/route-delivery.md) for implementation and acceptance; the static checker enforces a project convention, not a universal ranking rule.

Use [repair and validation patterns](../implementation-patterns/rendering-validation.md). A canonical added by JS without conflicting initial canonical is not automatically invalid. Dynamic rendering for crawlers is a workaround, not the preferred long-term architecture.
