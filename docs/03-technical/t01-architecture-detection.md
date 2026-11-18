# T01 — Website architecture and technology detection

Status: initial methodology and offline observation summarizer; behavioral evaluation pending. Source checkpoint: 2026-11-18.

## WHAT
Characterize the actual delivery chain of the authorized website, by route/template and environment. Separate technology (language, dependency, framework, router, CMS), generation strategy (build-time, request-time, client-time or mixed), hosting and observed delivery. A dependency is not a deployed runtime; SSR and SSG can produce identical initial HTML; hydration or a client component is not proof of CSR. Never equate a framework with an index result.

## WHY
The right repair depends on which layer owns the defect. A generic 200 fallback may be a hosting rewrite, an initial noindex may originate in a shared metadata template or HTTP header, and a missing product description may result from failed data loading. Migrating frameworks before locating the cause increases cost and risk without proving benefit. Google's crawler can render JavaScript but initial source, navigation and directives matter independently.

## WHEN / WHEN NOT
Use at onboarding, technical audits, rendering incidents and stack-specific implementation planning. For narrow known issues inspect relevant routes only. Do not probe unnamed hosts, private apps, admin URLs, hidden endpoints or infrastructure; do not install detectors, dependencies, run untrusted project scripts, or execute build/deploy commands without authority. If a working route satisfies its contract, no change is valid.

## INPUTS
Authorized origin/repository and mode, route purpose and expected access/status, environment and revision, known architecture and owners, permitted source files, lockfiles and build output, approved direct GET/DOM observations, redirects and HTTP headers, relevant search inspection when authorized. Use R06 stable page IDs and R09 locale scope. Do not copy secrets, cookies or private content into reports; record sanitized evidence references only.

## HOW

### 1. Identify the delivery chain and units
Record DNS/CDN/edge or reverse proxy (only authorized configuration or observed public response), router, app runtime, build output, data sources/CMS, metadata owner, cache and deployment. Split monorepo apps and public marketing, articles, products, locale routes, app dashboard and login. Trace one actual representative of each important template, not just homepage. Define expected public, intentionally excluded, protected, missing, moved and error behavior before interpreting search status. A public noindex utility is not an authentication mechanism.

### 2. Inspect code without execution
In scoped files inspect package.json or ecosystem manifests, resolved lockfile versions, framework config and route entrypoints, server/client entrypoints, static generation/revalidation, metadata/head helpers, build command definitions, static files and hosting redirects/rewrites. Inspect scripts as text first; package installation can execute arbitrary code and need network access. Use deployment configuration and exact revision to associate a build with an observed site. Declared semver ranges are not resolved versions. In a monorepo record the app root and which package actually owns each route. Do not search for credentials or log private env values. Inspect the least necessary files.

| Clue | Candidate interpretation | Limit |
|---|---|---|
| React or Vue dependency | UI library present in manifest | Not proof of site-wide CSR |
| Vite config or dependency | Build tooling or dev server integration | Vite supports static and SSR workflows |
| next dependency, app/ or pages/ | Possible Next.js and router conventions | Confirm actual config/version/build/deployment; route modes may differ |
| Astro, Nuxt or SvelteKit dependency | Candidate framework | Verify adapter/output and route configuration |
| CMS/backend templates | Candidate server-generated content | May also provide content to a static or headless frontend |
| HTML files in build directory | Candidate static output | Not proof deployed or that every dynamic route exists |
| Server header, script path, generator metadata | Public technology hint | Can be stale, absent, spoofed or inherited |

### 3. Observe actual delivery
Use approved direct GET with bounded timeouts; record requested URL, status and redirect chain, initial response headers (redact cookies/identifiers), raw source snapshot and environment. Do not follow cross-origin redirects outside authorization. Do not use HEAD alone as proof of GET behavior. For known public samples compare initial visible primary content with actual browser-rendered DOM after a documented readiness condition; inspect network/resource errors, console and mobile parity if available. Distinguish primary content from navigation, boilerplate, hidden JSON state, templates and scripts. A route with client-only transitions still needs a valid direct entry. Check page title, canonical, robots meta and X-Robots-Tag separately in their actual layers; record unexpected 200 shell for a known missing route. Private authorization tests require explicit approved synthetic fixtures or access tests; never attempt bypass. If streamed content is involved collect complete response where supported, not only first chunk.

### 4. Classify observed delivery separately from implementation
| Source / rendered primary content | Observation | Next check |
|---|---|---|
| Present / present | Initial content observed | Check consistency; SSG vs SSR remains unresolved without generation evidence |
| Absent or partial / present | Client completion observed | Check readiness, JS/resource loading, performance, discoverability and intent; could be progressive hybrid |
| Absent or partial / absent or partial | Incomplete in both tested states | Diagnose actual route/data/render errors or unmet test readiness |
| Present / absent or partial | Content regression after render | Investigate hydration/state and source/DOM disagreement |
| Missing capture / unknown | Insufficient evidence | Collect bounded observations; do not invent results |

Record declared generation strategy independently. Confirm SSG with actual route build output/generation configuration linked to deployment; SSR with request-time code/config and deployment evidence; CSR/hybrid with actual entry/render paths and observed behavior. A cache HIT is not SSG proof. Streaming, incremental regeneration, server/client component boundaries and runtime cache modes vary with versions and host; verify current official documentation. Do not assume all client components are missing initial HTML. If evidence differs across environments, retain distinct records, don't average or conflate.

### 5. Identify owners and route defects
Map observed inconsistency to likely owner, alternatives and next verification: CDN/edge rewrite, route mapping, server response, head generation, render/hydrate, data fetch, caching or source content. Prioritize credible exposure of private content or widespread eligibility failures; preserve authorization and investigate. Unexpected public initial noindex removed in DOM still requires source/header review; Google may skip rendering. Handle error pages honestly. Retain useful route URLs and functional UI. Start with smallest reversible fix; migration requires documented necessity, cost, route parity and separate approval. Use R08 for sequencing, existing [rendering protocol](../../decision-engine/rendering.md) and [route delivery](../../implementation-patterns/route-delivery.md) before stack-specific modules.

### 6. Offline observation summarizer
Use scripts/inspect_architecture.py with a prepared JSON envelope: schema_version "1", scope, declared_dependencies object of name/spec strings, and 1–500 routes with id, expected (public/private/missing/redirect), declared_strategy (csr/ssg/ssr/hybrid/traditional/unknown), status (integer HTTP status or null), source_content/rendered_content (present/partial/absent/unknown), initial_noindex/rendered_noindex/unauthorized_content_visible (boolean or null) and evidence_ref. Public means intended acquisition route here; do not feed intentional noindex utilities as intended indexable. Use sanitized synthetic or approved observations only. Source and DOM may come from a complete capture reviewed by an operator; the tool does not parse HTML, determine framework, fetch URLs, execute project code, infer actual generation strategy, validate redirects, or test authorization. Null must remain unknown. Findings are review candidates, not confirmed crawler penalties; status 200 on a missing route does not by itself prove Google selected a soft 404. CLI exit 0 means processed input, not no defects. Refuse non-finite JSON and duplicate keys on CLI ingestion. See [example](../../examples/architecture/README.md).

## VERIFY
Confirm target/app/template and deployment revision; lockfile versions vs declared ranges; representative direct entry and missing route; initial source vs actual rendered primary content; metadata/header and locale consistency; access expectations and evidence limits; status and redirect chain where permitted. For a verified issue document layer owner, smallest corrective action, acceptance and rollback. Do not claim browser, network or platform inspection ran when unavailable. Run offline tests and fixture separately from actual live checks. E39–E42 are public development cases, not independent competence evidence.

## MEASURE
Baseline by environment and template: sampled primary content availability, source/DOM agreement, accurate statuses, unresolved observations, verified defects and release regressions. Compare the same representative routes before/after and measure observed performance separately. Search-selected canonicals, processed index and traffic outcomes require authorized platform evidence and appropriate time windows.

## ADAPT
Static site: inspect generated paths and hosting rewrites. SPA: inspect deep-link server policy and client completion, not automatic replatform. SSR: inspect caching, request errors and private-data handling. Hybrid: classify per route, not one site label. CMS/headless: distinguish content source from frontend. New site: mark deployed behavior not yet observed; design acceptance first. No code access: public read-only observations and explicit unknowns. No browser/network: code/build evidence only; no claims about live delivery. Multilingual: verify route variants and RTL without converting language into market. Large sites: bounded stratified template samples, disclose gaps.

## RECOVER
If observed and declared architecture conflict, check exact deployment, cache, redirects and environment; preserve both observations and narrow scope. Missing capabilities remain blocked. Stop unsafe execution or evidence export. If a change regresses route status/access or content, stop release, use approved rollback and verify matched samples. Never force production reconfiguration based on a public fingerprint.

## OUTPUTS
[Architecture inventory](../../templates/architecture-inventory.csv), [architecture decision protocol](../../decision-engine/architecture-detection.md), [synthetic exercise](../../examples/architecture/README.md), route-level evidence and scoped prioritized next checks. Private target data stays outside the universal library.

## SOURCES — checked 2026-11-18
- [Google JavaScript SEO](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics): crawl/render/index boundaries, initial directives and server delivery guidance.
- [Vite static deployment](https://vite.dev/guide/static-deploy) and [SSR](https://vite.dev/guide/ssr): build tool supports different rendering/deployment models.
- [Next.js Server and Client Components](https://nextjs.org/docs/app/getting-started/server-and-client-components), [deployment](https://nextjs.org/docs/app/guides/deploying-to-platforms): component and deployment behavior; confirm target version and enabled features.
Route labels and input schema are internal diagnostic conventions, not ranking factors.
