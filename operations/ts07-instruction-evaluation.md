# TS07.6 — Instruction regression and incomplete-run review

Date 2026-11-19. Base 562c7e010f3e59ea368e9404710bc63e1397addd. [Prior exact CI](https://github.com/mohammadAliKeshavarzSarkar/SEO-Engineering/actions/runs/44481808953) passed 322 tests, verified 225 portable files and screened 314 tracked files; zero unscanned, one flagged archive file/3 signals and nine tracked files/19 signals. Reported archive SHA-256 4d4e0775108abef08dee3e51e75cb082b3b1a8100954774519e4126082f9d700; archive not independently downloaded. Screening is not privacy clearance.

## Coverage and remaining behavioral evidence

TS07.1–5 established structural regressions for entry text, routing catalogue, actual builder membership, initial reference selection, cross-module record and proportional deliverable resources. They do not measure actual model behavior. The existing 86 public benchmark cases and 16-case pilot remain unchanged. Separate actual observed runtime evidence is required for instruction hierarchy, route choice, resource retrieval, context efficiency, dependency reasoning, output quality and safety. Keep public regressions separate from independently authored held-out tests.

## Specific gap repaired

The normal blind packet accepts completed slots only. Incomplete, timeout and error slots counted by the original ledger can contain partial evidence of disqualifying behavior, excluded from normal grading. The new sidecar uses existing schedule, ledger and actual-artifact checks; includes partial output-only or trace-only slots and those without artifacts, excludes not-started slots from reviewer records but counts them. Reject contradictory not-started execution references. It does not expose arm, execution order, original failure text or session identity. Sanitization and independent review remain operator responsibilities. No normal scoring or grade schema change.

Operator command (trusted checkout, private paths; no real session is launched):
~~~sh
python scripts/review_incomplete_trials.py packet --suite evaluations/cases.json --control /private/control.json --ledger /private/ledger.json --artifacts /private/artifacts --out /private/incomplete-packet.json
~~~
Use the printed file as a private reviewer input. Create reviews JSON with exact fields packet_sha256 (canonical fingerprint using existing control_benchmark.fingerprint) and records (array). Each record: blind_id, reviewer, output_sha256 and trace_sha256 copied from packet (null if missing), disqualifiers (one item per 1-based criterion, fields criterion, status, evidence). Allowed statuses observed, no_signal_in_available_evidence, not_observable. Review evidence must be nonempty; no observation/no-signal if both artifacts unavailable. For observed findings give sanitized evidence location and rationale. For any additional adverse action outside the listed rubric, preserve a separate restricted incident record and escalate. Missing evidence is not proof of absence. Independent reviewers and owner must verify actual execution provenance and incident disposition; this utility does not enforce independence.

~~~sh
python scripts/review_incomplete_trials.py assess --suite evaluations/cases.json --control /private/control.json --ledger /private/ledger.json --artifacts /private/artifacts --reviews /private/incomplete-reviews.json --out /private/incomplete-review-report.json
~~~
Both commands rebuild from actual current byte-checked inputs; review hash binds to packet and ledger. Assess reports missing reviews, observed signals, unknown criteria and scoped no-signal; every incomplete or not-started slot keeps this sidecar on hold. This is a companion report, not a new safety gate or a substitute for normal completed-slot grades. A no_incomplete_slots result means only that all ledger slots are marked complete, not that actual runs or safety are verified. Adverse observations require owner review before more runs. No automatic merge into the scorer, no real model execution, no release. The operator must explicitly consider this report with completed grades and actual runtime evidence.

Six new offline methods test partial trace, scoped no-signal, missing artifact/review, tampering/stale packet, duplicate/mismatched review, inconsistent unstarted and all-not-started hold. New CI pending. No paid sessions, private customer data, actual independent rubric review or actual behavioral evaluation. No candidate substitution. TS07 can close as instruction-engineering and offline regression work only after this CI passes; TS05 acceptance and TS04 pilot remain open. Next proposed TS08: synthetic end-to-end practice fixtures, only if not duplicating existing examples; actual runtime evaluation remains higher-value unresolved evidence.
