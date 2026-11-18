# Benchmark grade input schema

Maintain this file format in a private evidence workspace. Do NOT paste invented responses or scores into real run records. The scorer operates on adjudicated grades only; it cannot determine whether a real reviewer or model produced them.

Top-level JSON object:
- plan_sha256: exact canonical plan fingerprint printed by prepare.
- runs: array of graded run records, one for each case_id, repeat, arm combination. Omit ungraded runs; report missingness and original run error in the experiment log.

Each record:
- case_id, repeat (positive integer), arm (baseline or skill).
- output_ref: actual sanitized response reference.
- trace_ref: actual trace/log reference, or explicit no-tool run record describing what was observable.
- reviewer: independent reviewer identifier.
- expected: array of objects with criterion (1-based position in the frozen case expected array), status (pass/fail/not_observable), evidence (actual response/trace citation and reason).
- disqualifiers: array of objects with criterion (1-based position in the frozen disqualifiers array), status (absent/observed/not_observable), evidence (reason and observable record).
Every criterion must appear exactly once. Keep blinded original ratings and label mapping outside agent access; use adjudicated records without inventing observations. A missing response remains ungraded, not a fictitious complete grade. A complete numeric result alone is not independent evidence. See [protocol](benchmark-protocol.md).
