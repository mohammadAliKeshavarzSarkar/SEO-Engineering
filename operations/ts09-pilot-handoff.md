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

## TS09.6 — Validate downstream activation-intake consistency

The handoff now accepts only the exact version-1 output envelope of `scripts/review_activation_evidence.py`. It rejects unknown fields, affirmative certification claims, malformed or duplicated baseline/skill trace inventory, inconsistent trace hashes and missing-trace declarations, and any status that disagrees with declared critical or unobservable findings. A consistent critical finding **escalates** rather than disappearing behind favorable completed grades. The output records `activation_intake_sha256` (canonical JSON SHA-256, or null if absent) so a private reviewer can compare the precise submitted summary used by this handoff.

This check only authenticates *internal consistency and the supplied summary's digest*. It cannot independently verify that the summary came from the intake tool, that original trace bytes were genuinely observed, or that the operator used independent permissions. Retain the private original intake, pair record and traces for separate authorized review; do not pass raw traces into this handoff. Invalid input fails without writing an output file. Synthetic unit tests include contradictions, missing trace evidence, escalation and unsupported approval claims. No actual runtime activation, scored pilot, independent authorization or release has been completed.

## TS09.7 — Full private artifact-root inventory (fail closed)

`scripts/prepare_trial.py check_artifacts` now checks *every* entry within the supplied dedicated artifact root, not just the exact paths referenced in the ledger. Existing byte/hash and UTF-8 checks remain. A valid root contains only folders corresponding to the frozen blind slot identifiers and the fixed `output.txt` / `trace.txt` files explicitly declared by that ledger; empty known slot folders are permitted. Unexpected top-level files or directories, nested directories, symlinks and unreferenced partial evidence cause a nonzero failure rather than silently dropping material that could change a safety review. An `artifact_inventory_complete: true` field is emitted only on successful validation. An all-not-started slot cannot have execution references.

Do **not** automatically delete an unexpected artifact to make validation pass. Preserve and investigate it privately, reconcile against actual observed execution and hashes, and use a separately reviewed fresh evidence root where appropriate. Restrict the directory to the single frozen pilot, outside the agent-visible workspace, source checkout and other candidates. Name/type enumeration is not a guarantee against concurrent filesystem mutation, forged ledger data, trace semantics or successful OS read isolation; an authorized reviewer still checks provenance and privacy. The pilot remains **HOLD** for actual independent execution and owner decisions.

## TS09.8 — Independent reviewer and adjudication integrity

The former scoring path could consume a favorable adjudicated grade packet without validating it against the two original blind reviews. Maintainers can now submit two original completed-run grade packets (`--first-review` and `--second-review`) and, if applicable, an `--adjudication-resolutions` packet to the consolidated pilot handoff. Original packet and final grades are each matched against the *freshly regenerated*, byte-verified blind packet from the same control and ledger. Both original reviews must be provided together; scoring without them remains a visible `completed_independent_reviews_missing` hold.

```sh
python3 scripts/check_pilot_handoff.py \
  --suite evaluations/cases.json \
  --control /private/pilot-operator/control.json \
  --ledger /private/pilot-operator/ledger.json \
  --artifacts /private/pilot-operator/artifacts \
  --grades /private/grades-adjudicated.json \
  --first-review /private/grades-reviewer-a.json \
  --second-review /private/grades-reviewer-b.json \
  --adjudication-resolutions /private/grade-resolutions.json \
  --out /private/handoff-reviewed.json
```

The separate `scripts/review_completed_adjudication.py` command also accepts `--packet`, `--first`, `--second`, `--adjudicated`, optional `--resolutions`, and `--out` for a preliminary private review. Its result binds canonical SHA-256 digests of all four packets, counts reviewer overlap, records unresolved disagreements and missing coverage, and preserves original `observed` disqualifier signals **even when final adjudication declares `absent`**. Those signals escalate in the consolidated handoff. Consensus cannot silently be overridden; an observed disagreement requires an explicit matching resolution or remains held.

A resolution file has exactly `packet_sha256`, `first_sha256`, `second_sha256`, `adjudicated_sha256` and `records`. Each record is `blind_id`, `kind` (`expected` or `disqualifiers`), 1-based `criterion`, `selected_status`, `adjudicator` and `rationale`. Only actual disputed criteria may be resolved. The adjudicator identifier must differ from the two original reviewer identifiers for that slot, but **identifier inequality is not verification of human identity or independence**. Preserve the originals and evidence in a restricted private store. If no disputes exist, omit `--adjudication-resolutions`. If reviews are missing, original observations unobservable, or disagreements unresolved, hold. A consistent synthetic report never authorizes paid model calls, distribution, a stable release or a safety certificate.
