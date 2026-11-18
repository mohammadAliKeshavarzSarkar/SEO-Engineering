# Technical audit and release gates

## Audit stages

0. Scope/authority: agreed origin, environments, goals, owners, data boundaries. Baseline current site and search/analytics where access exists.
1. Inventory: canonical routes and intended state, template, source/rendered HTML, HTTP behavior, redirects, robots, sitemap, links. Compare representative URLs and enumerate edge cases.
2. Diagnose and prioritize: reproduce each issue; evidence, affected templates, impact, severity, confidence and dependency. Check whether issue is live or only a code observation.
3. Implement: small reversible changes; preserve stable URLs and UX; use branch/PR and decision record; test locally.
4. Pre-release: [release checklist](../../templates/release-checklist.md), review crawl/render/schema, mobile, forms and consent. Block privacy, security, widespread eligibility and critical function regressions.
5. Deploy and sample production via GET, browser, search inspection and analytics. Verify sitemap and canonical alignment. Record release annotation, owner, monitoring and rollback decision.
6. Measure after appropriate crawl/report latency. Distinguish eligibility passed, indexed, ranking and business outcome. Don't declare final success based on a build.

## Checklist severity

P0: important pages blocked or returning wrong status broadly, personal data transmitted, compromised site. P1: canonical mismatch/soft 404 on meaningful template or conversion failure. P2: incomplete content/links, performance degradation or trust gaps. P3: optional rich result, preview polish, experiments. Escalate by actual reach/context. Record reproducer, expected vs actual, evidence and owner in [issue template](../../templates/audit-finding.md).

Use the local static checker as a narrow smoke test. Production verification still requires network, browser and authorized search/analytics tools.
