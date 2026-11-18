# Rendering and information architecture

Before selecting or changing a rendering approach, use [T01 architecture detection](t01-architecture-detection.md) and the [technical roadmap](technical-roadmap.md). Framework dependencies do not prove actual delivered rendering strategy.

For source/render discrepancies and browser readiness use [T02](t02-javascript-rendering.md). Do not equate an incomplete or missing capture with absent primary content.

For React/Vite and browser routing, use [T03](t03-react-vite-spa.md); keep concrete build artifacts separate from deployed status and routing evidence.

For Next.js, use [T04](t04-nextjs-hybrid.md): inspect router, version, cache model and deployment separately; full streamed response and ready DOM are not early stream prefix.

## Choose the rendering approach by template

| Approach | Good fit | Tradeoffs |
|---|---|---|
| CSR | Authenticated highly interactive surfaces; public pages only after validation | JS execution, initial loading, status/head consistency |
| SSG / pre-render | Stable public marketing and article routes | Build freshness, dynamic route enumeration, invalidation |
| SSR | Dynamic public content that needs current HTML | Runtime cost, caching and availability |
| Hybrid | Different needs by route | Operational complexity and consistent contracts |

Google can execute JavaScript. Choose pre-render or SSR when it improves reliably delivered content, response codes, social sharing and performance; do not migrate frameworks by default. Avoid serving materially different content only to crawlers. Each public route needs stable URLs, real anchors with href, accessible navigation and primary content that does not require interaction to become discoverable. Dynamic UI can hydrate after initial HTML. Avoid contradictory initial and JS-updated canonicals. If an intended indexable page has noindex in its initial response, do not rely on JavaScript to remove it: Google may skip rendering after detecting noindex. Check HTTP X-Robots-Tag as well as source and DOM. Check titles, descriptions, canonical, robots, body and structured data in source and DOM. Test history navigation, deep links, invalid routes and hydration on mobile.

## Architecture

Create page inventory by purpose, audience, template, intent, canonical and index policy. Link each important page from other relevant pages. Topic hubs should expose real useful resources rather than thin filter shells. Use descriptive anchors and breadcrumbs where helpful; labels should be accessible. For each resolved task and locale, select an intended primary destination under [R06 page mapping](../02-research/r06-keyword-to-page-mapping.md); preserve distinct useful pages and leave unresolved tasks unassigned. This is strategic planning, not canonical selection or a one-page-per-keyword rule. Cross-link where it helps users. Avoid orphans and chains of near-identical pages. Pagination should have crawlable component URLs and appropriate canonical handling. For infinite scroll, provide discoverable paginated equivalents where needed.

## Implementation acceptance

Direct GET to each route type delivers a meaningful status and consistent canonical; valid content in rendered HTML; links discoverable without interaction; mobile content parity; interactive behavior intact. Inspect production as well as local build. Static assertions do not prove indexation.

Sources: [JavaScript SEO](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics), [crawlable links](https://developers.google.com/search/docs/crawling-indexing/links-crawlable), [pagination](https://developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading).

For a practical stack-neutral implementation contract, use [route delivery](../../implementation-patterns/route-delivery.md).
