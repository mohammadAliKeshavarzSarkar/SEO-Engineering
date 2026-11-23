# TS09.5 — Consolidated pilot evidence handoff

Date 2026-11-23. Base `720abac62937d1eb2803f0e3b82f67d64d81d1b3`. The latest baseline [CI](https://github.com/mohammadAliKeshavarzSarkar/SEO-Engineering/actions/runs/45115328900) passed 375 offline tests. **No actual Cursor/Codex pilot execution, private held-out grading, owner approval or independent runtime review has occurred.**

The existing benchmark scorer handles completed sessions; the incomplete-trial sidecar reviews errors, timeouts and partial trace evidence. Those were independently correct but could be read separately. This maintainer-only `scripts/check_pilot_handoff.py` collects the actual byte-checked artifact summary and binds both reviews to the **same** frozen control and ledger, optionally including the [unscored activation intake](ts09-activation-intake.md). It deliberately never approves a pilot or a release. It does not perform live inference, network access, sandbox testing or evidence of reviewer independence. It prevents a favorable completed-run metric from concealing observed disqualifiers in incomplete sessions.

## Private operator command

~~~sh
python3 scripts/check_pilot_handoff.py \
  --suite evaluations/cases.json \
  --control /private/pilot-operator/control.json \
  --ledger /private/pilot-operator/ledger.json \
  --artifacts /private/pilot-operator/artifacts \
  --grades /private/graded-completed.json \
  --incomplete-reviews /private/graded-incomplete.json \
  --activation-intake /private/activation-intake.json \
  --out /private/pilot-handoff.json
~~~

Optional inputs may be omitted **only when not yet available**; missing applicable completed grades, incomplete safety reviews and activation evidence appear as hold reasons. A missing reviewer result must never be substituted with a fabricated record. The consolidated report includes source commit and archive identities, exact control/ledger hash, verified supplied artifact count, execution statuses, ordinary completed-grade summary, incomplete safety review, contradictions, hold reasons and escalation reasons. It does not include raw trace or output content. Keep the private operator/grade packets out of the model's workspace and out of the repository.

## Decision logic

| State | Example | Output |
|---|---|---|
| All slots not started | No model execution | Hold |
| Partial/error/timeout | Missing independent safety review | Hold |
| Incomplete partial disqualifier observed | Evidence of critical behavior outside completed grades | Escalate to owner |
| Completed skill critical disqualifier observed | Safety criterion in grader output | Escalate to owner |
| All fictional grades pass | No independent execution/activation/privacy approval | Hold for independent owner review |
| Candidate/trace tampering | Incorrect hashes or disjoint frozen records | Reject input |

**No combination of local records can set pilot_approved or release_approved true.** Actual independent execution, trace semantics, reviewer independence, filesystem permission boundaries, privacy/rights, economics and owner decisions remain separate. The pilot is still 16 public pairs/32 planned sessions; full public benchmark and independently authored private held-out tasks are not complete. Explicitly selected source, model and environment must be recorded before any real session. This TS09.5 step is a safety handoff improvement, not observed behavioral performance or a stable release.

Run regression suite; seven new synthetic tests exercise actual local file-byte checking, favorable grading, incomplete review, escalation, mutation and candidate identity. CI pass required. Frozen prior candidate unchanged. No BeatFit or WebsiteBotScroll changes.
