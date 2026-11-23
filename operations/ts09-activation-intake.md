# TS09.4 — Private activation evidence intake

Date 2026-11-23. Initial source: `5dba09c1d7fd76ee356c2cfcd0756746c5018625`. **No model sessions executed.** This is maintainer-side bookkeeping for the still-pending real unscored activation and isolation probes, not a model runner, actual trace-semantic verifier or safety authorization.

## What to collect privately

Use two **separate disposable copies** of the original staged first-pair workspaces for unscored synthetic probes. Preserve sanitized UTF-8 trace copies *outside* the model-visible workspace and source tree at `<evidence>/baseline/probe.txt` and `<evidence>/skill/probe.txt`. Obtain independent observation notes and the exact runtime/model/settings and authorization record. Do not copy credentials, real customer information or rubrics.

A JSON record has exactly these top-level keys: `control_sha256`, `candidate_commit`, `archive_sha256`, `runtime_kind`, `operator`, `authorization_ref`, `probes`. The first four bind to the frozen first-pair staging record; `probes` contains exactly `baseline` and `skill`. Each arm has `runtime_version`, `model`, `settings_ref`, `session_ref`, `trace_ref`, `trace_sha256`, `discovery`, `entrypoint_read`, `routed_reference_read`, `unrelated_activation`, `read_isolation`, `tool_permissions`, `observation_ref`.

- Discovery/read fields and `unrelated_activation`: `present`, `absent`, `unknown`.
- `read_isolation` and `tool_permissions`: `verified_by_operator`, `failed`, `unknown`.
- Trace identity: `baseline/probe.txt` or `skill/probe.txt`, and SHA-256 of submitted sanitized bytes. For missing trace use null for both ref and digest; this prevents a passed review.

Unscored probes should record that baseline lacks the treatment skill and treatment discovers, reads its entrypoint and reads a routed reference. Both arms should use the same model, settings and runtime version, separate sessions, no unrelated activation, and independently checked permissions/read boundaries. A self-report from a model or mere presence of a file is **not** trace evidence.

## Intake command from the same clean checkout

~~~sh
python3 scripts/review_activation_evidence.py \
  --operator /private/pilot-operator \
  --workspaces /isolated/pilot-workspaces \
  --record /private/unscored-probe-record.json \
  --evidence /private/unscored-sanitized-traces \
  --out /private/activation-intake.json
~~~

The original first-pair ledger must remain **all not started**: only its disposable copies may be used for unscored probes. The script rechecks staging via the existing `check_pilot_staging.py`, requires exact record bindings, validates the two privately submitted traces at fixed paths and retains only hashes and dispositions in its output. It never runs an agent, interprets a runtime event schema or rewrites the pilot ledger.

| Disposition | Meaning |
|---|---|
| `escalate_to_owner` | Baseline unexpectedly sees skill, treatment misses expected read, extra skill activated, failed permissions/isolation, or unmatched model/settings |
| `hold_missing_or_unobservable` | Missing trace or unknown observation; cannot presume success |
| `ready_for_independent_review` | Submitted bytes match and declarations are internally consistent. **Not a verified activation or approval to run scored sessions** |

An independent runtime/operator reviewer must inspect actual trace meaning and effective tool/read boundaries; explicit owner permission and costs remain required. All outputs explicitly set runtime activation, isolation, paid pilot and release certification false. Sample unit tests use fictional strings and do not establish agent performance. See [TS04 operator procedure](ts04-runtime-launch.md) and [pilot staging](ts09-pilot-staging.md). Existing scorer, public pilot selection and benchmark candidate remain unchanged.
