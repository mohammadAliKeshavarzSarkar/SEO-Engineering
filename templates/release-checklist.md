# SEO release checklist

Project / candidate revision / environment / reviewed route scope / owner / date:

This is a target-website checklist, not a skill distribution approval or blanket requirement to run every test. Select applicable tests before release. Use T11's exact subject/assertion binding where a deployment gate is required. Record separate pre-release and post-release observations; no production access, deployment or external submission is authorized by this checklist.

| Test area | Expected assertion (adapt to scope) | Actual evidence / stage | Status |
|---|---|---|---|
| Page intent and URL policy | Approved inventory preserved or migration separately approved | | not-run |
| Delivery | Intended canonical, redirect, missing, private and variant routes return expected status/access; private access asserted separately | | not-run |
| Rendering and declarations | Matched source and render checked where applicable; intended content, canonical, robots and metadata consistent | | not-run |
| Discovery | Relevant links, sitemap policy, meaningful lastmod and required resource access verified | | not-run |
| Experience | Applicable mobile, deep links, hydration, keyboard and reduced-motion checks | | not-run |
| Structured data | Accurate visible facts, appropriate vocabulary and feature eligibility checked separately | | not-run |
| Media/performance | Applicable baseline and regression guardrails | | not-run |
| Business functionality | Approved synthetic success, rejection and retry cases; accepted outcome distinct from event receipt | | not-run |
| Consent/analytics | Approved consent and actual collection, deduplication, data minimization verified when relevant | | not-run |
| Data and security | Scope, access, public artifact/log review; no private data exposure | | not-run |
| Post-release | Authorized production sample; separate processed search observation and outcome monitoring where available | | not-run |

Statuses: pass, fail, blocked, not-run, N/A (explain why genuinely inapplicable). Missing tooling or permission is blocked, not N/A; never turn pending post-release checks into pre-release passes. Record test ID and exact subject, evidence, exceptions, material unresolved risk, rollback owner and independent release decision. A local check cannot establish live, indexed or business outcome status. Use [deployment regression](../workflows/deployment-regression.md) for structured gates and [agent run record](agent-run-record.md) for actual observations. Do not promote an unsafe release because a majority of checks pass.
