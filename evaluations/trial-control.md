# TS04 — Controlled pilot and independent review

Status: infrastructure and public pilot cohort prepared; no actual model responses or independent grades. This extends the existing [benchmark protocol](benchmark-protocol.md), not a replacement for it.

## Fixed pilot

[Public pilot](public-pilot.json): 16 known cases, one repeat, 16 pairs / 32 planned individual sessions. Purpose is to test the workflow, identify high-severity failures and estimate review effort; not representative or held-out. Cases selected by the author for varied research, technical, privacy, release and recovery behavior. Full public suite remains 86 cases, three repeats = 258 pairs / 516 sessions planned. Held-out cases must be independently authored and kept private, frozen before execution.

## Control workflow

Use fresh private output paths; never commit control, ledger, reviews or traces. `scripts/control_benchmark.py` is maintainer-only, not in the portable utility allowlist. Fill the [configuration](trial-control-config.example.json) with an actual model/runtime/settings, verified candidate commit and archive SHA-256, common prompt/context fingerprint, treatment and identical budgets. Select one actual experiment variant in advance. For the public pilot prevent access to rubric-bearing files with an independently reviewed restricted workspace; record exact restrictions and candidate deviations, and do not treat it as an unmodified release test. The controller requires a rubric_restricted declaration for public runs but cannot enforce it. For held-out work use unmodified candidate and independent private cases.

```sh
python3 scripts/control_benchmark.py schedule --suite evaluations/cases.json --config /private/config.json --cohort evaluations/public-pilot.json --out /private/control.json
python3 scripts/control_benchmark.py dispatch --suite evaluations/cases.json --control /private/control.json --blind-id RUN_ID --out /private/task.json
python3 scripts/control_benchmark.py blind --suite evaluations/cases.json --control /private/control.json --ledger /private/ledger.json --out /private/review-packet.json
python3 scripts/control_benchmark.py finalize --suite evaluations/cases.json --control /private/control.json --ledger /private/ledger.json --grades /private/blind-grades.json --out /private/result.json
```

- Schedule: seeded pair order, balanced within-pair arm order, independent shuffled presentation order, opaque labels. Keep operator-only control confidential. Give only dispatch prompt and identical common context to each fresh isolated session; install skill only in treatment. Record actual order, settings, deviations, tool activity, time/budget and when skill activation cannot be proven. Use no live customer site.
- Ledger: object with control_sha256 (canonical JSON fingerprint printed by schedule) and runs array. Exactly one record per blind_id, even failures or unstarted slots. Record status completed/incomplete/timeout/error/not_started, session_ref, environment_ref, output_ref, output_sha256, trace_ref, trace_sha256, failure_reason. For completed slots nonempty refs, 64 lowercase hex digests and null failure_reason; for other slots provide nonempty reason, use null for unavailable fields. Hash actual sanitized artifact bytes externally and use arm-neutral reference names. No retries replacing failures; new experiment if needed.
- Blind: generate packet containing prompt, criteria and sanitized output/trace references and hashes, without structured arm identities or original run ordering. Operator verifies actual bytes and removes obvious arm identifiers from presentation where doing so does not change evidence; preserve originals privately and record imperfect blinding. Do not share control/ledger or label mapping. Independent reviewer accesses actual sanitized records, never model self-scores.
- Grades: object with packet_sha256 (fingerprint printed by blind) and records array. Each record blind_id, reviewer, output_sha256, trace_sha256, expected, disqualifiers. Grade arrays use the [grade schema](benchmark-grades.md); adjudicate independently, retain disagreements and original ratings privately. Incomplete execution or absent grade cannot be counted as passing.
- Finalize: verify frozen plan, all-slot ledger, packet/grade identities and artifact hash declarations; map grades back to pairs only after review. Keep critical failures, matched rates, paired outcomes and failure/missingness by arm. Unobserved runs remain visible. The tool checks supplied metadata, not artifact bytes, real session independence, actual review quality, privacy, blinding or claims. Human review is essential.

No API credentials or autonomous inference; no external agent sessions accessible in current authoring environment. No efficacy claim until actually run. Initial pilot results must not be pooled with independent holdout. Define a practical meaningful improvement and guardrails before launch, review paired regressions even if average improves, and avoid tuning on held-out material. Actual external activation, privacy, source review and owner approval remain separate.

