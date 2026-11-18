# v0.3.0 — Advanced technical SEO engineering

Status: development; v0.2.0-rc.1 remains pinned at 0483ff33d73687adccd11408ec26318c880ceddf. Stable release gates from [stabilization](../08-learning/stabilization.md) remain outstanding. New technical modules do not certify the previous candidate.

| ID | Module | Deliverable | State |
|---|---|---|---|
| T01 | [Architecture and technology detection](t01-architecture-detection.md) | Route evidence, ownership, offline observation tool | Initial methodology |
| T02 | [JavaScript rendering engineering](t02-javascript-rendering.md) | Matched source/render observations, readiness, repair patterns and offline QA | Initial methodology |
| T03 | [React, Vite and SPA SEO](t03-react-vite-spa.md) | Concrete route registry, metadata, build/host patterns and local artifact QA | Initial methodology |
| T04 | [Next.js and SSR/SSG/hybrid](t04-nextjs-hybrid.md) | Router/cache model, runtime/export compatibility, streaming and freshness QA | Initial methodology |
| T05 | [Crawling and robots](t05-crawling-robots.md) | Robots interpretation, discovery and sitemap review, crawl-budget evidence and scoped offline QA | Initial methodology |
| T06 | [Indexing and canonical engineering](t06-indexing-canonicals.md) | Eligibility, canonical conflicts, historical processed evidence and scoped offline QA | Initial methodology |
| T07 | [URLs, redirects and migrations](t07-url-migrations.md) | Identity policy, reviewed map, GET trace/graph QA and rollback | Initial methodology |
| T08 | [Metadata and structured data](t08-metadata-structured-data.md) | Reviewed typed drafts, safe serialization, literal capture and layered feature QA | Initial methodology |
| T09 | [Core Web Vitals and performance](t09-performance.md) | Separate field p75, matched lab QA, bottleneck attribution and UX preservation | Initial methodology |
| T10 | [Technical audit automation](t10-audit-automation.md) | Fixed offline T01–T09 runner, native evidence, scoped review groups and R08 triage | Initial methodology |
| T11 | [Deployment and regression prevention](t11-deployment-regression.md) | Reviewed release policy, candidate and production evidence gates, offline gate evaluation | Initial methodology |
| T12 | [Technical troubleshooting](t12-technical-troubleshooting.md) | Incident investigation, competing hypotheses, scoped evidence and recovery review | Initial methodology |

Use the [module standard](../01-foundations/module-standard.md). Verify framework and platform versions before implementation. Begin with existing useful architecture; no automatic migration. Keep all examples synthetic and private data outside library. Unit/CI success does not establish actual index or agent outcomes.

## Optional external evidence providers

Technical modules specify evidence needs independently of a vendor. WebsiteBotScroll may become an optional source through a jointly reviewed versioned contract. The exact 0.1.0 schema and fixtures are pending; do not create provider mappings or assume operational capabilities. Preserve standalone tools, project context and evidence limitations. REST/MCP and actual integrations remain deferred.

## Technical development exit and stabilization

All twelve initial modules are authored as of dev.12. This is a development milestone, not certification. Before a technical release candidate, review cross-module terminology and failure semantics, test adversarial inputs and combined cases, run exact-revision repository/package checks, inspect sources and actual package contents, and record unresolved external/behavioral gates. See [technical stabilization plan](technical-stabilization.md). Do not replace the pinned historical candidate or assume external compatibility.
