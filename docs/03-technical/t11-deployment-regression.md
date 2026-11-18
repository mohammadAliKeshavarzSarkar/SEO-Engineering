# T11 — Deployment and regression prevention

Status: initial review methodology and offline gate evaluator. No live deployment, CI integration with a target site, monitoring, provider adapter, rollback execution or behavioral certification. Research checkpoint 2026-11-18.

## WHAT

Prevent avoidable regressions across source, built artifact, preview and production. Define explicit acceptance gates before implementing changes, bind evidence to the actual release subject, and keep the final deployment decision with an authorized owner. Applicable to static sites, SPAs, server-rendered/hybrid systems, CMS and migrations. This is not a universal scoring system.

## WHY

A passing build is not proof of correct routing at the CDN, rendered content, production directives, access control or search processing. Environment variables, caches, middleware, edge rewrites, CMS publishing and feature flags may differ across deployments of the same commit. Small, separately verifiable changes reduce diagnosis and recovery ambiguity.

## WHEN / WHEN NOT

Use for releases that can change public URL behavior, templates, rendering, content, assets, privacy, tracking or route configuration. Choose a proportional reviewed scope. Do not require irrelevant diagnostics for a copy-only change. Do not deploy, change access, run unauthorized live probes, or mutate search-platform settings from the offline report. If the current release is healthy and a change is unsubstantiated, no-change is valid.

## INPUTS

Authority and owner; change set and intended route registry; explicit test coverage and criticality; current revision, artifact/deployment identity, environment/origin, capture profile and configuration reference; baseline evidence; release and rollback plans. Keep stable route IDs and exact URLs in the private inventory. Record separately the preview and production intents, including intentionally private/nonindexable paths. Use T10 for underlying module reports, not its process exit code as a gate.

## HOW

1. Review the change differential: routes/templates, redirects, middleware, headers, rendering mode, metadata, robots/sitemap, resources, consent, conversions and locale-sensitive UI. Pick impacted representative routes and critical edge cases, including public, excluded, private and missing routes. Document untested scope.
2. Predeclare gate IDs, required/optional status, method, owner, evidence criteria and baseline. Requirements are project policy, not platform scoring. A required unrun or failed check holds readiness; do not retroactively downgrade it to get a pass. Use a separate approved policy revision if scope genuinely changes.
3. Validate local code and build output (unit tests, declared route inventory, T03/T08 and applicable checks). Pin the build inputs and output identity. Record failures, tool availability and timeouts. Do not run untrusted PR code with privileged secrets. Keep CI logs and artifacts free of private payloads and credentials.
4. Validate an authorized preview with its own policy. A private preview should be protected by access controls; crawler directives are not authorization. For intentionally indexable production routes review the actual effective response status, robots decisions, header and initial/rendered directives, canonical, content and links. Do not remove intended exclusions globally. Use T02/T05/T06/T07/T08 rather than invent a second diagnostic system.
5. Before release, record candidate evidence subject and applicable mandatory results, reviewer, intended deployment, rollback compatibility and remaining gaps. Candidate review does not prove production behavior. A person or authorized release system makes the deployment decision separately.
6. After release, create a separate production gate manifest bound to the actual deployed subject. Check approved GET traces, representative rendered DOM/mobile behavior, effective headers, sitemap/robots, canonical and conversion/privacy paths where relevant. Cache and feature flags may alter behavior: record profile/configuration and actual identity, not just source revision. Do not test private data through public search tools.
7. In production, escalate confirmed access exposure independently of ordinary gate results. Stop expansion of affected rollout and engage the authorized incident owner. For material regressions compare matched baseline evidence; choose safe containment, compatible rollback or forward fix. Rollback can be harmful when migrations, persistent state, URL changes or privacy fixes cannot be reversed safely.
8. Reverify after a fix or rollback with a new subject. Retain old reports unmodified and link the incident, decision and evidence. Track search indexing/traffic and field performance separately, on suitable windows from T06/T09; delayed reporting is not a failed deployment test by itself.

### Gate review matrix

| Check family | Candidate review | Production review |
|---|---|---|
| Public route status/redirect | Build and preview expectations | Actual scoped HTTP response and final target |
| Indexability and canonical | Expected route policy, source/render checks | Effective headers, source/render, robots and canonical |
| Private route access | Authorization tests without real sensitive payload | Approved production access test, escalate confirmed exposure |
| Content and navigation | Representative templates and missing route | Ready DOM, links, locale, functional UI |
| Performance | Matched lab profiles and agreed tolerance | Matched samples; delayed field evidence separate |
| Measurement | Synthetic events and consent QA | Authorized non-sensitive event checks, separate reporting delay |

Gate policy may mark a check optional or omit it as inapplicable with reviewed rationale. Required coverage must reflect the actual change, not simply the shortest available test list. An optional failure still needs review; no automatic release approval.

### Local evidence contract

Run `python3 scripts/review_release_gates.py --input examples/deployment-regression/sample.json --output release-gates.json`. Standard library; strict JSON keys and duplicate/non-finite rejection; new output path required. Input schema_version "2"; release_id and policy_ref nonempty strings; subject object with stage candidate/production, scope_ref, revision, artifact, environment, profile, config_ref, all nonempty strings. Gate array with unique IDs, required bool, rationale, assertion, and evidence (null or object). Evidence contains subject (same shape), outcome pass/fail/incomplete, ref, policy_ref, gate_id and assertion. A supplied observation is current only if its whole subject, policy_ref, gate_id and assertion all exactly match the reviewed gate. Scope_ref is an opaque reviewed scope identifier, not an independently verified URL inventory. Schema v1 is historical and rejected; re-review evidence and rebuild v2 inputs, never populate missing bindings from assumptions. Exposure is separately null or an object with the same subject and ref, recording a supplied confirmed unauthorized access observation. A mismatched exposure receives investigation escalation, not an assertion about the current deployment.

Result includes per-gate state pass/fail/incomplete/missing/stale, preserved evidence, blockers and optional review IDs, and exposure status. Disposition is escalate for supplied exposure (current or stale), hold for unresolved required evidence, review_optional for unresolved optional evidence, ready_for_owner_review otherwise. At least one required gate is mandatory. This evaluates supplied declarations, not their truth, timestamp freshness, authorization, completeness or validity of referenced artifacts. Operator must establish those separately. Exit zero indicates processing, not readiness. No arbitrary paths or commands embedded in input. Reports contain refs and project identifiers; store outside public Git when sensitive.

## VERIFY

Use the synthetic fixture: required candidate evidence matches and an optional check is missing, so disposition is review_optional. Required missing, incomplete, failed or stale evidence holds. Known or stale exposure escalates independently. Candidate evidence cannot satisfy production checks. Invalid schema, duplicate IDs/keys, missing required check or unsafe output overwrite fail. The offline utility neither collects evidence nor validates claims. Explicitly report unrun network/browser/platform stages.

## MEASURE

Track reviewed required coverage, unresolved gaps, repeat regressions, time to detection and safe recovery against comparable releases. Treat these as operational metrics, not ranking factors. For SEO outcomes compare actual processed search and field evidence after suitable windows with confounders noted. Never fabricate improvement or interpret gate readiness as actual search eligibility of all pages.

## ADAPT

Static sites: verify route-to-artifact plans and hosting fallbacks. SPA: verify host routing, ready DOM and true error behavior. Hybrid/CMS: record cache rules, configuration/content revision and runtime dependency changes. Migration: retain T07 mapped redirects, old/new origin checks and compatible rollback. High-risk data-sensitive sites: test synthetic accounts and protect observations; missing access test is a blocker when required. Low-risk changes may use narrower representative coverage with explicit rationale.

## RECOVER

Stop on missing authorization, evidence mismatch or suspected exposure. Do not automatically change directives or undo migrations; involve release/security/data owners. Preserve evidence in a restricted store and recheck the exact newly deployed subject. Escalate unresolved production incidents to the troubleshooting workflow.

## OUTPUTS

Reviewed gate inventory, candidate and production manifests/reports, release decision, scope and residual risk, incident/rollback plan, verification and measurement record. Use [deployment workflow](../../workflows/deployment-regression.md), [gate inventory](../../templates/deployment-gate-inventory.csv) and [decision record](../../templates/decision-record.md).

## SOURCES

Checked 2026-11-18: [Google technical SEO guidance](https://developers.google.com/search/docs/fundamentals/get-started) (crawl controls versus index exclusions; crawlable resources); [Google site moves](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes) (review temporary directives, redirects and monitoring). Gate status model, CI evidence identity and ownership are internal engineering policy, not search-engine requirements. Recheck provider/platform and framework-specific behavior at implementation.
