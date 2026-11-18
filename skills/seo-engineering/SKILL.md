---
name: seo-engineering
description: Research, audit, design, implement and validate evidence-based SEO for websites; use for technical SEO, rendering, search intent, content, structured data, analytics and search visibility decisions.
---

# SEO engineering skill

## Inputs and outputs

Inputs: target origin, repository/build access, hosting, route inventory, market and business goals, available search/analytics evidence, task scope. Missing inputs must be recorded as unknown, not guessed. Work read-only unless asked to implement. Output: prioritized findings, sources and dates, alternatives, decision, change plan, acceptance criteria, test evidence, limitations and next action.

## Workflow

1. Read `../../docs/01-foundations/operating-principles.md` and `../../docs/01-foundations/evidence-and-decisions.md`. Resolve paths from this skill's directory or repository root. Select task-specific modules from the root README.
2. Baseline: gather GET responses for representative routes, source and rendered HTML, sitemap, robots, redirect variants, crawl and index reports, performance and conversion data where authorized. Do not infer live behavior from source code alone.
3. Research: primary docs first; SERPs and competitors for market questions; record region, device, date and limitations. Map intent to URLs; resolve overlaps based on evidence.
4. Decide: classify each recommendation, severity and confidence. Use `../../templates/decision-record.md`. Present real alternatives and costs; avoid premature framework migration.
5. Implement the smallest approved reversible patch; preserve canonical URL stability, visual design, interaction and accessibility. Avoid duplicate metadata or events. Do not change production or publish private data without authorization.
6. Validate: run the appropriate static and browser tests; verify deployed HTTP behavior, search inspection, mobile parity, structured data, consent and event deduplication where applicable. Use `../../templates/release-checklist.md`.
7. Report: what changed, what was tested, failures, unknowns, expected outcome, measurement interval, rollback and documentation update. Search success cannot be guaranteed.

## Guardrails

No made-up search volumes or positions, fake authors/schema/reviews, link schemes, doorway pages or bulk thin AI content. No user health data or PII in analytics. Never treat tools' scores as ranking factors. Verify current feature eligibility in the source register; historical source documents may be outdated.
