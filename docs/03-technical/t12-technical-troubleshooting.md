# T12 — Technical troubleshooting and incident recovery

Status: initial methodology and executable offline incident ledger. No live investigation, causal inference, monitoring, deployment, external adapter or behavioral certification. Checkpoint 2026-11-18.

## WHAT
A scoped incident procedure for technical SEO, traffic anomalies, search appearance, rendering, migrations, performance and measurement. A symptom is not a cause; a restored technical assertion is not a restored business or search outcome. The same method works for a single route, template or site but conclusions must stay within sampled scope.

## WHY
Several independent changes can coincide with search or conversion loss. Aggregate position, clicks and traffic mix can conceal very different effects. A deployment timestamp is a lead, not causal proof. Blind fixes may remove useful features or reverse a privacy/security correction. Test competing explanations and prefer reversible, discriminating checks.

## WHEN / WHEN NOT
Use when a material unexpected deviation, failed T11 gate or unresolved T10 finding requires investigation. Do not manufacture an incident from an intentional exclusion or normal uncertainty. Escalate credible unauthorized access or safety concerns promptly to the appropriate owner; do not perform further intrusive tests without authority. Do not trigger broad crawls, migrations, indexing requests or rollback automatically.

## INPUTS
Approved target, incident owner and scope; exact intended behavior, symptom, onset/timezone, recent changes, baseline and affected cohorts, deployment/config/profile identity, raw evidence and limits, actual capabilities, current containment and recovery constraints. Separate analytics, search property, host logs and browser evidence. Use synthetic/redacted records in public examples; preserve sensitive evidence outside Git.

## HOW

1. Establish the symptom: source, comparison period, expected versus actual, coverage, severity and confidence. Record absolute timestamps, data freshness, filters, aggregation and known reporting gaps. Separate immediate technical hazards from business-impact hypotheses.
2. Contain confirmed exposure or widespread critical failures with authorized owners before pursuing growth or ranking explanations. Preserve restricted evidence. Do not infer authorization from robots/noindex. Do not assume a previous release is safe; examine rollback compatibility with state, migrations, security and URLs.
3. Scope the blast radius: affected and unaffected comparable routes, template, locale, device, environment and change boundary. Review same weekdays, seasons and query mix if relevant. Establish current live behavior separately from historical indexed inspections. Avoid extrapolating a sample to every URL.
4. Form competing hypotheses, including a nontechnical or measurement explanation when plausible. State a mechanism, predictions on affected/control cohorts, a falsification condition and the smallest useful next test. Prioritize evidence by its ability to discriminate, safety and cost. Do not assign arbitrary causal probabilities.
5. Collect authorized evidence with T01–T09 or T10. For every hypothesis, record reviewed supporting/refuting/inconclusive observations, exact context and limits. Conflicting or unmatched evidence remains unresolved. Evidence association is not proof: review alternatives, temporal order, plausible mechanism and reproducibility. A reviewer records any confirmed cause and its uncertainty separately.
6. Compare no-change/monitor, targeted fix, containment, forward fix and rollback. Select the smallest authorized response addressing the evidenced issue. Record expected results, owner, risks and rollback constraints. Do not change stack, canonical policy, all directives or URL structure merely to test a theory.
7. Verify on the intended recovery deployment with T11 and relevant native checks, using affected and control cohorts. Compare results against original expected behavior; missing or stale checks are unresolved. A passing release or static check cannot supersede outstanding exposure.
8. Keep later search processing, clicks, field performance and business outcomes in separate follow-up records. Use appropriate reporting latency and matched cohorts, without promising recovery dates. Close only with an authorized owner decision, explicit residual risks, evidence scope and follow-up responsibility. Reopen on recurrence.

### Symptom-specific playbooks

| Symptom | First discriminate | Evidence and next step |
|---|---|---|
| Organic click loss | Report completeness, demand and query/page mix vs eligibility/appearance | Compare Search Console segments, data anomalies, Trends and recent changes; T05/T06/T08 plus actual affected/control routes |
| Analytics organic sessions or leads drop | Consent/measurement/attribution vs true search or conversion loss | Compare independent Search Console data and approved event/backend checks; preserve denominators and data gaps |
| New public route absent from index | Live access/status/robots/noindex/render vs historical processing, intended duplicate or unmet value | T02/T05/T06; compare last crawl to deployment, live vs indexed; do not repeatedly submit as default |
| Template blank or links missing | Source vs ready DOM, resource/network failures, hydration or route fallback | T01–T04, matched captures, errors and route controls; no automatic SSR migration |
| Wrong canonical or soft 404 | Intent, content equivalence, effective status, redirects and signals | T06/T07; check missing and real URL separately; don't force all URLs to home |
| Migration loss | Old/new mapped cohorts, redirect traces, wrong target, temporary directives, processing lag | T07; retain mappings and safe rollout; restore only compatible fixes |
| Performance degradation | Matched lab evidence vs field cohort, cache/config change and bottleneck | T09; isolate LCP/INP/CLS causes; preserve accessibility and interactions |
| Snippet or rich appearance changes | Actual search result vs declared metadata and eligibility | T08; check observed output and feature scope; display is not guaranteed |
| Geo/device-only error | Environment/profile/locale/CDN/cache/WAF differences | Match authorized captures and verify affected and control routes; no crawler impersonation or access bypass |
| Private access exposure | Actual authorization defect, not index rules alone | Escalate to security/data owner; contain safely, check authorized synthetic access and separate exposure closure |

### Local incident ledger
Run scripts/review_incident.py with a reviewed JSON manifest; see [fictional fixture](../../examples/technical-incident/README.md). Schema_version "2", incident_id and scope_ref nonempty strings. subject and recovery_subject (null if unplanned) each contain scope_ref, revision, artifact, environment, profile, config_ref, all nonempty strings; scope_ref must equal incident scope. Evidence entries have unique id, subject, ref, quality ("complete" or "partial") and verification (null or object with check_id, assertion and outcome pass/fail/incomplete). These are reviewer declarations, not verified captures. Hypotheses have unique id, claim, falsifier, and assessments linking unique evidence IDs to "supports", "refutes" or "inconclusive". Unknown refs are invalid. Only complete exact-subject evidence contributes to the diagnostic summary; unmatched/partial IDs remain excluded and visible. Supports plus refutes yields conflicting; either alone yields support_only or refute_only, otherwise unresolved. These descriptions do not confirm or dismiss a cause.

Recovery checks have unique id, required boolean, assertion, evidence_id (null if missing) and outcome ("pass", "fail", "incomplete", or null if missing). Evidence is current only if complete and exactly matches the recovery subject; it must additionally have a verification object matching the check ID, assertion and outcome. Otherwise report unmatched_or_partial or unmatched_assertion. Schema v1 is historical and rejected: re-review evidence before rebuilding manifests; do not fill new verification objects without actual assertion-specific review. At least one required check for a declared recovery subject; without a recovery subject checks must be empty. Missing/mismatched/partial/incomplete/failed required checks block recovery review; optional gaps are explicit. Exposure_ref null or a nonempty restricted reference to a reported exposure requiring independent escalation; absence does not prove safety. Search_follow_up is "pending", "not_applicable" or "unknown"; actual search outcome is never inferred by this tool. Provide the actual scope/coverage, timestamps, source reliability and authority in underlying reviewed records. An offline ledger cannot verify those references or their truth.

Disposition: escalate when any exposure_ref is supplied; investigate for absent recovery subject or unresolved required check; review_optional when only optional gaps remain; technical_recovery_review otherwise. This does not establish causality or incident closure. Historical diagnostic contradictions can coexist with a verified fix; they remain in the ledger for human review.

## VERIFY
Synthetic normal and adverse cases: simultaneous support/refutation, unmatched and partial evidence, unknown references, duplicate identifiers, missing verification, wrong recovery subject, and exposure even with passing checks. Fresh report path; no network, source execution, arbitrary paths in input or external data access. Exit zero means processed; report false for automatic cause confirmation and incident closure. A passing test is not an investigation of a real site.

## MEASURE
Time to detect, contain and restore the scoped behavior; recurrence and residual scope; search and business trends separately with reporting limits. Never treat a single cohort or score as impact proof. Establish predeclared observation windows and owner review, not guaranteed ranking return.

## ADAPT
Small sites may need a few selected pages; larger sites need justified sampling by route families and failure signatures. SPA/hybrid sites require T02–T04; multilingual sites may have locale-specific failure modes; migrations depend on T07 and state compatibility. For missing inspection/analytics access, disclose limitations and use approved local/live tests where possible, not fabricated data.

## RECOVER
Stop unauthorized actions. If fix fails, preserve before/after evidence and reopen hypotheses rather than add uncontrolled changes. Contain with appropriate owner; re-evaluate rollback compatibility. If technical checks pass but search outcomes have not, maintain follow-up rather than blindly revert. If exposure is resolved, the owner records restricted incident disposition separately; this ledger never clears an exposure automatically.

## OUTPUTS
[Incident workflow](../../workflows/technical-incident.md), [decision procedure](../../decision-engine/technical-incident.md), [incident record](../../templates/incident-record.md), private evidence references, reviewed hypotheses, scoped recovery checks and owner decision with remaining follow-up.

## SOURCES
Reviewed 2026-11-18: [Google search traffic drop diagnosis](https://developers.google.com/search/docs/monitor-debug/debugging-search-traffic-drops), [URL Inspection](https://support.google.com/webmasters/answer/9012289), [crawl troubleshooting](https://developers.google.com/search/docs/crawling-indexing/troubleshoot-crawling-errors). These support multiple competing causes, reporting and live/index distinction, and host availability investigation. Ledger and procedural gates are internal engineering policy; no live property or search claim.
