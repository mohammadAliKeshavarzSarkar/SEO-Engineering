# Task routing

## Locate library root L

In a portable installation, use the references/library directory inside this skill if its docs/01-foundations/operating-principles.md exists. Otherwise, for a full SEO-Engineering checkout, use the repository root two levels above the skill directory. Confirm expected docs/, templates/ and decision-engine/ exist. If neither is present, report missing resources; do not pretend the skill is complete. Paths in the table are relative to L, not the target website.

Read docs/01-foundations/operating-principles.md and docs/01-foundations/evidence-and-decisions.md for material decisions. Do not load the entire library by default.

| Task or trigger | Load relative to L |
|---|---|
| New website, broad strategy | workflows/new-website.md; docs/02-research/r01-business-and-positioning.md; docs/06-operations/audit-and-release.md |
| Keyword discovery | docs/02-research/r01-business-and-positioning.md; docs/02-research/r02-keyword-discovery.md; docs/02-research/research-roadmap.md |
| Search intent, SERP analysis | docs/02-research/r03-search-intent-and-serp.md; decision-engine/search-intent.md; templates/serp-snapshots.csv; templates/serp-results-v2.csv; templates/intent-assessments.csv |
| Keyword normalization and clustering | docs/02-research/r04-keyword-normalization-and-clustering.md; decision-engine/keyword-clustering.md; templates/keyword-cluster-review.csv; scripts/cluster_keywords.py |
| Competitor intelligence and competitive gaps | docs/02-research/r05-competitor-intelligence.md; decision-engine/competitor-intelligence.md; templates/competitor-register.csv; templates/competitor-search-footprint.csv; templates/competitor-page-benchmark.csv; templates/competitor-opportunities.csv |
| Page mapping and topical gaps | docs/02-research/market-and-keywords.md; docs/02-research/research-roadmap.md; docs/02-research/r05-competitor-intelligence.md; use specialized modules as they become available |
| Persian or multilingual | docs/02-research/persian-and-international.md |
| Crawl/index/status/robots/sitemap | docs/03-technical/crawl-and-index.md; docs/06-operations/troubleshooting.md |
| JS rendering or SPA/SSR | decision-engine/rendering.md; docs/03-technical/rendering-and-architecture.md |
| URL, canonical, redirect, migration | docs/03-technical/urls-and-migrations.md |
| Content, trust, metadata | docs/04-content/on-page-and-editorial.md |
| Structured data/social/entity | docs/04-content/structured-data.md |
| Images, video, Discover | docs/04-content/media.md |
| Performance, mobile, accessibility | docs/03-technical/performance.md |
| Search platform data, logs | docs/05-measurement/search-platforms.md |
| Analytics, lead, ecommerce events, consent | docs/05-measurement/analytics.md; docs/05-measurement/privacy-and-qa.md |
| Local, ecommerce, SaaS or programmatic | docs/07-specialties/site-types.md |
| AI search | docs/07-specialties/ai-search.md |
| Traffic loss or diagnostic | docs/06-operations/troubleshooting.md; relevant evidence guides |
| Authority | docs/04-content/authority.md |
| Experiment/monitoring | docs/06-operations/experiments.md |
| Implementation and QA | implementation-patterns/README.md; docs/06-operations/audit-and-release.md; templates/release-checklist.md |
| Skill updates/competence | docs/01-foundations/module-standard.md; evaluations/README.md |

If multiple triggers are relevant, resolve dependencies (privacy/security -> eligibility -> research/intent -> implementation -> measurement; baseline measurement can begin earlier). For narrow tasks do not mandate unrelated modules. If a future specialized document is not present, use the existing foundations and current evidence and report the gap.
