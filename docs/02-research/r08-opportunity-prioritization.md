# R08 — Opportunity scoring and prioritization

Status: initial agent-ready methodology and offline decision-support utility; behavioral evaluation pending. Source checkpoint: 2026-11-18.

## WHAT

Prioritization selects the next justified actions under the project's objectives, capacity, uncertainty, dependencies and risk. Separate a defect (observed mismatch to an expected requirement), incident (urgent actual or credible suspected harm), opportunity (hypothesis of beneficial change), investigation (evidence gathering), prerequisite and experiment. A high-volume query is not a task or a business impact estimate. A score is a comparison aid for eligible discretionary work, not a Google metric, a forecast, permission or universal action order.

## WHY

Research creates more possible work than teams can execute. Preserve useful existing behavior, protect users and business outcomes, handle critical defects first, then allocate limited effort to evidence-backed improvements. Google's technical requirements establish eligibility, not guaranteed indexing. Its traffic-drop guidance distinguishes widespread technical and security problems from ordinary fluctuations and cautions against radical changes to well-performing pages. Product prioritization methods such as RICE inspire consistent comparisons, not search ranking rules.

## WHEN / WHEN NOT

Use after or during R01–R07 when assembling a research, implementation, incident or maintenance backlog. Critical issues can interrupt the sequence. Use for new and existing sites, but do not require a growth score to repair urgent harm, meet legal/contractual obligations or investigate a credible incident. Do not deploy from a ranked list. Never score prohibited, deceptive or unsupported work into eligibility; do not disguise missing data as zero impact or guaranteed gain.

## INPUTS

Authorized target, task mode, objectives and accepted outcome metrics; relevant R01–R07 deliverables; reproducible technical findings, source/date/scope, affected page templates and audience; actual outcomes, opportunity hypothesis and confidence; effort range including engineering/editorial/review/QA/monitoring; risks, urgency, dependencies, owner, capacity, approvals and rollback. Preserve observations, estimated effects and assumptions separately. Use comparable target, objective, horizon and effort unit; do not combine incompatible markets, horizons or first-party/vendor measures.

## HOW

### 1. Create actionable records

Deduplicate findings referring to the same underlying defect or overlapping work. Group template-level fixes where appropriate; do not double-count affected pages or user reach. Split independent work from prerequisites and subsequent experiments. Record current/expected state, why it matters, affected audience and routes, evidence, outcome, mechanism, alternatives including no-change, owner, effort, risk, acceptance, rollback and review date. Keep the original research IDs and map them to backlog records. A task can be required without an immediate measurable search-volume estimate.

### 2. Severity and gates precede scoring

Use existing repository severity conventions (P0–P3). Confirm the intended index policy before labeling a noindex defect; intentional authentication is not an incident. Record actual severity versus suspected severity and narrow verification. 
| Tier | Typical situation | Handling |
|---|---|---|
| P0 | Credible serious privacy/security issue, broad broken public access or widespread unintended eligibility loss | Urgent triage, isolate/contain as appropriate and escalate to authorized owners; verify cause; approved safe remediation. No growth score. |
| P1 | Important template or accepted conversion path fails, material eligibility or measurement defect | Prioritized repair or urgent prerequisite investigation/review; no growth score. |
| P2 | Useful optimization, architecture/content improvement, measurable performance or discovery opportunity | Eligible discretionary work only after gates. |
| P3 | Optional refinement/experiment | Compare with other eligible discretionary work; do not treat as mandatory. |

P0/P1 labels are internal conventions. Severity depends on actual scope, business importance and user harm, not number of URLs alone. A credible P0 must remain visible even when evidence, authority or prerequisites are missing. Do not perform unsafe changes to resolve an incident; escalate and identify safe containment and verification. P1 investigation/review/blocked items still outrank unrelated discretionary growth in resource planning; queue labels alone are not a calendar.

Fit gate: reject out-of-scope, deceptive, duplicate, unsupported or prohibited growth proposals; defer unknown fit pending evidence. For a credible incident, distinguish the harm from any unapproved remediation proposal. 
Evidence gate: high confidence = reproducible observations or well-supported task and mechanism with relevant scope and alternatives; medium = useful scoped evidence with gaps; low = weak/indirect or incomplete evidence; unknown = absent. These are qualitative internal categories, not calibrated probabilities. Low/unknown requires bounded investigation; urgency is independent.
Risk gate: consider privacy, access, security, accuracy, accessibility, migration, dependencies, reversibility and business disruption. High or unknown risk requires review and approved mitigation/rollback, not a simple penalty in a score. Lower risk does not remove authorization. 
Dependency gate: identify prerequisite IDs and acceptance conditions; reject circular or missing references. Verify completed prerequisites with evidence before unlocking work. Excluded prerequisites require replanning, not bypass. An unresolved dependency on urgent incident must be escalated, not silently deferred. Track delays and capacity separately.

### 3. Estimate comparable impact and effort

Agree on a primary objective and horizon (e.g. next quarter), relevant measurement and team capacity before scoring. Use a transparent ordinal impact rubric combining expected reach and importance of the improvement; do not multiply by reach again. Example internal rubric: 1 = narrow useful improvement; 2 = limited audience/task benefit; 3 = material benefit to a defined audience or template; 4 = major benefit to important user journey or several relevant templates; 5 = substantial benefit to primary objective across meaningful scope. Define local anchors with owner and evidence before use. The scale is ordinal, not money or probability; do not claim a score of 4 is literally twice the benefit of 2. Avoid mixing outcomes that matter to different objectives without explicit tradeoffs. If impact is unknown, leave null.

Record expected reach separately with denominator, source and time horizon where known (e.g. eligible page cohort, observed users, qualified leads). Separate demand estimates from actual visits and conversion; no fabricated revenue or arbitrary CTR uplift. If adequate first-party data exists, a scenario estimate can describe incremental visits and conversion using explicit assumptions, aligned baseline, plausible ranges and guardrails. It is not a promise. For new sites, use justified qualitative impact and label missing historical outcomes.

Estimate low/high total person-days including research, implementation, coordination, editorial review, testing, release and follow-up. Person-days measure effort, not elapsed calendar time; dependency and staffing constraints add scheduling effects. Unknown effort is null, never zero. Split oversized uncertain tasks into evidence gathering and implementation. Do not game the rubric by splitting trivial tasks or concealing shared prerequisite costs.

### 4. Compare eligible discretionary candidates

Initial internal heuristic (adapted from impact/confidence/effort and informed by RICE, not identical to RICE):
S = impact × confidence weight / effort.
Use impact integer 1–5, medium confidence weight 0.5, high 1.0; low/unknown unscored. Effort in person-days with minimum 0.25. For effort range [L,H], report low score = impact × weight / H, high score = impact × weight / L, and mid score using (L+H)/2. These are sensitivity bounds over effort only; not statistical confidence intervals and not a complete model of uncertainty. If impact/confidence is uncertain, vary assumptions separately; document rank reversals and treat overlapping ranges as a reason for review. Compare only within the same objective/horizon and rubric. Optional work with no evidence or high/unknown risk remains outside scoring. Do not treat a low score as proof of no value.

Example A: impact 4, high confidence, 2–4 days → scores 1–2, midpoint-effort score 1.33. B: impact 5, medium confidence, 2–6 days → 0.42–1.25, midpoint-effort score 0.625. A is an initial candidate first; ranges overlap. Review strategic dependencies, feasibility, obligations, capacity and evidence before approval. A critical incident never competes with these scores.

### 5. Sequence work and document decisions

Maintain separate queues for incidents, repairs, eligible growth, risk review, investigations, blocked, excluded and verified tasks. Within growth, use the score as a discussion starter; P2/P3 are compared in the common discretionary queue, not automatic severity sequencing. Across queues do not blindly use report order: urgent triage/repair/dependency resolution takes precedence, and investigations that unblock high-value work may outrank ready growth. Select a small reversible batch consistent with available skills/capacity. Reserve incident capacity, coordinate shared templates, avoid simultaneous changes that obscure diagnosis, and record intentional overrides with rationale. No dependency is satisfied merely by its estimated score or written plan. 
For each selected task define decision status, owner, acceptance criteria, next action, validation stages and measurement. Include rejected and deferred work with reasons and revisit triggers. Prioritize experiments using learning value and guardrails; using no-change or a small measurement task is valid.

### 6. Offline utility contract

Use scripts/prioritize_opportunities.py with a JSON array of records: id, severity (P0–P3), status (pending/verified), fit (eligible/unknown/excluded), risk (low/medium/high/unknown), confidence (low/medium/high/unknown), impact (1–5 or null), effort_days ([low,high] or null), depends_on (IDs). The input must reflect one agreed objective/horizon/rubric; the script does not infer or verify these, authorization, true risks, source evidence or completed dependencies. verified means prerequisite acceptance confirmed; inconsistent verified status with unmet prerequisites or noneligible fit is rejected. It validates IDs, dependency references/cycles, enums and numeric ranges. It outputs separate lanes, unmet dependencies, reasons, optional score ranges and review/authorization reminders. Output sort is a deterministic presentation convention, not an execution schedule. P0 is kept in incident lane with blockers; P1 repair requires fit/evidence/risk/dependency checks even without effort/impact estimates. Priority of blocked/review P1 work is a human coordination decision. No network, deployment, forecast, optimization of a resource-constrained schedule or automatic approval. See scripts README or [synthetic exercise](../../examples/opportunity-prioritization/README.md).

## VERIFY

- All items trace to source IDs, current condition, user/business objective and target scope; assumptions distinguished from evidence.
- P0/P1 risks and prerequisites visible before discretionary work; private or intentionally nonindexed areas protected.
- Rejected or unsupported proposals unscored; high/unknown risk requires owner review; low/unknown evidence and missing estimates stay unscored.
- Dependencies valid and acyclic, acceptance evidence for verified prerequisites; no dependent execution before prerequisites.
- Scoring consistent objective/horizon, impact anchors, confidence and effort ranges; unknowns null; overlap and sensitivity discussed.
- Selected work records acceptance, owner, capacity, approval, verification, rollback and measurement; no ranking guarantee.
- Run deterministic utility tests and fixture checks; behavioral E27–E30 require independent model evaluation. Separate planned, implemented, verified and outcome states.

## MEASURE

Track time to triage/resolve material defects, accepted verification results, open dependencies, delivered versus estimated effort, evidence quality, meaningful outcomes and unintended regressions. Establish matched query/page cohorts or appropriate conversion/task metrics and baseline before approved changes; review after reasonable crawl and reporting lag. Do not attribute uncontrolled before/after changes solely to a task; evaluate confounders and guardrails. Compare predicted qualitative impact bands with observed outcomes where possible, revise rubric and effort estimation over time, and retain failed experiments. Score movements are not SEO performance.

## ADAPT

Greenfield: unknown search history; prioritize eligibility, useful launch paths and measurement contracts before speculative growth. Ecommerce: template reach and actual stock/conversion, navigation and promotional timing; avoid counting every variant as incremental demand. SaaS/B2B: qualified lead and adoption journeys may outweigh high-volume information; support and usability count. Local: legitimate offering and service coverage gates; compare markets separately. Multilingual/Persian: separate localized evidence, constraints and review effort; do not extrapolate foreign keyword estimates to local demand. Health/finance: safety and validated evidence are gates; never trade them away for score. Enterprise: cross-team dependency and rollout risk; use separate capacity planning and incident procedure. Small team: narrow scope and transparent coarse bands; no elaborate scoring required for obvious decisions.

## RECOVER

If new evidence changes fit, severity or expected effect, reclassify and preserve history, not silent score rewriting. If estimates are uncertain or ranks unstable, investigate or choose reversible steps. If prerequisite fails, block dependent work and reassess alternatives. If incident escalates or release fails, stop discretionary changes, invoke owner-approved rollback/containment and verify recovery. If no evidence of benefit, preserve no-change, record uncertainty and avoid escalating purely because work was completed. Do not enter private project records in public library.

## OUTPUTS

[Opportunity backlog](../../templates/opportunity-backlog.csv), [priority review](../../templates/priority-review.md), [decision protocol](../../decision-engine/opportunity-prioritization.md), [synthetic exercise](../../examples/opportunity-prioritization/README.md). Handoff to authorized implementation/release workflow. For current live site issues use troubleshooting and release guides; do not let research sequence delay necessary triage.

## SOURCES — checked 2026-11-18

- [Google technical requirements](https://developers.google.com/search/docs/essentials/technical): minimum eligibility is not indexing guarantee.
- [Google traffic-drop debugging](https://developers.google.com/search/docs/monitor-debug/debugging-search-traffic-drops): technical/security issues, diagnosis, contextual comparisons and avoiding unnecessary radical changes.
- [Google people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content): relevance/usefulness and reliable original content.
- [Intercom RICE prioritization](https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers): product planning inspiration; RICE separately includes reach, unlike this combined impact rubric.

All tiers, weights, impact anchors, effort bounds and queue ordering are internal defaults. No official ranking score, projected traffic or commercial assurance. No actual target website was audited or changed.
