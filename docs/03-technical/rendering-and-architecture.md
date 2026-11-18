# Rendering and information architecture

## Choose the rendering approach by template

| Approach | Good fit | Tradeoffs |
|---|---|---|
| CSR | Authenticated highly interactive surfaces; public pages only after validation | JS execution, initial loading, status/head consistency |
| SSG / pre-render | Stable public marketing and article routes | Build freshness, dynamic route enumeration, invalidation |
| SSR | Dynamic public content that needs current HTML | Runtime cost, caching and availability |
| Hybrid | Different needs by route | Operational complexity and consistent contracts |

Google can execute JavaScript. Choose pre-render or SSR when it improves reliably delivered content, response codes, social sharing and performance; do not migrate frameworks by default. Avoid serving materially different content only to crawlers. Each public route needs stable URLs, real anchors with href, accessible navigation and primary content that does not require interaction to become discoverable. Dynamic UI can hydrate after initial HTML. Avoid contradictory initial and JS-updated canonicals. Check titles, descriptions, canonical, robots, body and structured data in source and DOM. Test history navigation, deep links, invalid routes and hydration on mobile.

## Architecture

Create page inventory by purpose, audience, template, intent, canonical and index policy. Link each important page from other relevant pages. Topic hubs should expose real useful resources rather than thin filter shells. Use descriptive anchors and breadcrumbs where helpful; labels should be accessible. Keep one primary page per intent where sensible, with cross-links only when they support the user's next step. Avoid orphans and chains of near-identical pages. Pagination should have crawlable component URLs and appropriate canonical handling. For infinite scroll, provide discoverable paginated equivalents where needed.

## Implementation acceptance

Direct GET to each route type delivers a meaningful status and consistent canonical; valid content in rendered HTML; links discoverable without interaction; mobile content parity; interactive behavior intact. Inspect production as well as local build. Static assertions do not prove indexation.

Sources: [JavaScript SEO](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics), [crawlable links](https://developers.google.com/search/docs/crawling-indexing/links-crawlable), [pagination](https://developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading).
