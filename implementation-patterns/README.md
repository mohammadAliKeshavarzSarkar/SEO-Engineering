# Implementation patterns

Patterns are adaptable starting points, not patches to blindly copy. Select the target stack and hosting first; honor established architecture and code conventions. Do not claim these contracts are framework-specific implementations.

| Concern | Reusable contract | Common failure | Verification |
|---|---|---|---|
| Route registry | One authoritative mapping of indexable route, canonical, metadata and content identifier | Sitemap and rendered head drift | Compare emitted files, direct GET and DOM |
| URL redirects | Direct permanent mapping from moved URL to true replacement | Loop, home fallback, lost safe params | GET representative aliases and invalid paths |
| Content rendering | Primary content and links discoverable without user action | Loading-only shell or interaction-gated content | Initial HTML and rendered browser checks |
| Metadata | Route-aware title, canonical, social fields and index policy | Homepage canonical on all routes | Template-level assertions + live source and DOM |
| Schema | Stable entity IDs, actual visible facts, supported type | Invented reviews or stale prices | Schema and feature validators, human review |
| Performance | Measured media priority, bounded JS, stable layout | Lazy LCP, long tasks, layout shifts | Lab diagnostics plus field data |
| Conversion | Accepted event following real business outcome, idempotent | Click counted as successful lead | Accepted/rejected/retried requests, consent, reconciliation |

Before writing code, inspect real project configuration and current dependencies. Use official framework/hosting references for exact API syntax and version. Existing scripts/audit_html.py and scripts/check_docs.py provide narrow offline smoke tests; they are not a live crawler. Document acceptance, failure modes, security/privacy, compatibility and rollback for new patterns. Include synthetic fixtures in examples, tests where deterministic and behavioral evaluation cases where agent judgment matters.

- [Route delivery and metadata](route-delivery.md): stack-neutral source/render/status implementation contract, minimal repair decisions, synthetic HTML and acceptance checks.

- [JavaScript rendering repair and validation](rendering-validation.md): navigation semantics, initial/DOM consistency, readiness-aware local browser acceptance and failure cases. Browser code is illustrative, not executed.

- [React, Vite and SPA route delivery](react-vite-spa.md): version-aware metadata and prerender patterns, hosting/base routing, artifact and browser acceptance. Illustrative framework examples, not executed deployments.

- [Next.js delivery and cache validation](nextjs-delivery.md): version-aware App/Pages models, metadata ownership and reviewed freshness samples. Framework snippets are illustrative, not compiled or deployed.
