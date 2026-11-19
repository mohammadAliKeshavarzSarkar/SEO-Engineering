# Advanced technical stabilization

Checkpoint: dev.12 initial development completed; TS03 targeted portable installation hardening. Corrected TS02 exact-commit CI passed; TS03 changed-commit CI and wider gates must be checked separately. This is not certification.

| Stage | Work | Exit evidence |
|---|---|---|
| TS01 | Cross-module inventory; consistency of scope, statuses, evidence semantics, privacy/authority and router precedence | Reviewed issue register, fixes, explicit remaining gaps (initial targeted review recorded; comprehensive semantic review remains) |
| TS02 | Adversarial and integration fixtures; malformed, stale, partial, contradictory observations and scope mismatch | Adverse fixtures, expected assertions and exact-revision results (targeted corrections committed; verify changed-commit CI separately) |
| TS03 | Portable package and runtime acceptance | Exact archive/source match, reproducibility in pinned runtime, content review, external activation if available (offline acceptance strengthened; external activation not run) |
| TS04 | Behavioral evaluation | Independent baseline/skill and held-out runs, blind review and failure records, not public-case counts alone |
| TS05 | Source review and candidate readiness | Current primary-source review, privacy and license/owner gates, versioned candidate if justified |

Follow [existing stabilization policy](../08-learning/stabilization.md) and [release review](../../templates/skill-release-review.md). A missing external tool or owner approval remains blocked. Do not conflate technical stabilization with WebsiteBotScroll contract development; preserve standalone boundaries.

## TS01 audit record

Base: dee89f229633d28867f23f37510667f32f1cbd58. Recursive Git tree was complete (245 tracked blobs). [Exact base CI](https://github.com/mohammadAliKeshavarzSarkar/SEO-Engineering/actions/runs/44302047350) succeeded. Inspected T10–T12 code and tests, sampled all nine native utility interfaces/scope and escalation layouts, execution contract, evidence foundations, builder/verifier and CI. This is a targeted review, not line-by-line review of all files, complete semantic or source/privacy audit. No live target, independent model execution or provider contract inspected.

| ID | Finding (base revision) | Correction / test |
|---|---|---|
| TS01-01 | T11 evidence matched only release subject; passing evidence could survive changed policy, gate ID or assertion or be copied to another gate. Scope was not explicitly bound. | Schema v2 scope_ref and policy/gate/assertion binding; tests for changed policy/assertion/ID, cross-gate reuse and legacy rejection. |
| TS01-02 | T12 recovery evidence matched only subject and complete quality; existing positive test reused HTTP evidence for a distinct rendered assertion. | Schema v2 assertion/outcome-specific verification; replace positive fixture test with separately declared rendered evidence, reject mismatched assertion and old schema. |
| TS01-03 | T10/T11/T12 output/exit status semantics were documented separately; no consolidated handoff contract. | [Technical handoffs](technical-handoffs.md), execution contract routing note and explicit non-equivalence. |
| TS01-04 | Portable smoke compared output bytes, but identical unintended semantics can still pass parity. | Add expected T10/T11/T12 output semantic assertions to repository and extracted package checks. |

Six new regression test methods plus changed positive recovery test and semantic smoke assertions. These are authored, not claimed passed until changed-commit CI is verified. Contract changes are intentionally breaking only for the two unreleased local schema v1 inputs; historical candidate untouched. Source version remains dev.12 with exact revision pin; no new distribution candidate.

Remaining for TS02: adversarial input shapes, T10 invalid grouping/report preservation (including exposure), full representative cross-module fixtures, malformed timestamps/identities and input bounds; review how assertions map to real evidence and coverage; no automatic integration. Wider source/semantic/privacy/behavioral and external runtime gates remain outstanding.

## TS02 adversarial and integration record

Base: cc52b196dcf363e56704ae5defd0fae24209b133. [Exact base CI](https://github.com/mohammadAliKeshavarzSarkar/SEO-Engineering/actions/runs/44302501575) succeeded. Container checkout was blocked by DNS resolution; verification of this change relies on exact-revision hosted CI. Reviewed T10 grouping/error paths, R08 dependency validation, T11/T12 reviewed binding and package verification. No live collection or external integration.

| ID | Finding / scenario | Correction and expected regression outcome |
|---|---|---|
| TS02-01 | Invalid/stale/cyclic grouping previously discarded the complete T10 report | T10-v2 rejects grouping batch and writes native reports, ungrouped candidates and independent escalation; exit 2, no triage |
| TS02-02 | Malformed shared audit envelopes were not checked for exact shape | Exact envelope/task keys and digest validation before diagnostics; reject invalid inputs; expected native module failure isolated |
| TS02-03 | Cross-module exposure or incomplete verification could be misread as success | Synthetic reviewed handoffs: exposure escalates T11/T12, scope/profile/config/policy/stage changes hold release, unrelated or partial evidence blocks recovery; no automatic mapping |
| TS02-04 | Package parity lacked a combined adverse audit exercise | Add adverse fixture: T01 suspected exposure, T02 validation failure, rejected stale group; expected eight processed, one failed, escalation retained, exit 2 in both layouts |
| TS02-05 | Reviewed T11/T12 identifiers could contain lone Unicode surrogate code points | Reject malformed identifiers and invalid shapes; valid Unicode remains accepted |

Added five T10 and six cross-module test methods (11 new), updated previous invalid-group expectations, and added semantic/parity checks of adverse fixture. Authored tests are not claimed passed until this exact revision CI is inspected. T10 input schema remains v1 with exact keys; report method changes to T10-v2 and exit 2 now covers grouping rejection. T11/T12 local v2 shapes unchanged. Do not treat this as exhaustive fuzzing, full site or search evaluation, or verified contents/provenance of reviewed references. Actual timestamps and coverage in underlying evidence remain a manual obligation; broader native malformed input paths and operational workloads remain future review. TS03 next: package and external runtime acceptance, with actual external agent activation and wider content/privacy and behavioral reviews still separate.

First TS02 execution: [CI for 6ae667977832eaa9d9cae2e99d669eabd898f1c0](https://github.com/mohammadAliKeshavarzSarkar/SEO-Engineering/actions/runs/44461733371) ran 255 unit tests, 254 passed and one failed (`test_invalid_shared_envelope_is_rejected`). Log inspection showed the test helper treats None as a request for the default fixture; corrected the test to call audit directly with each malformed value. All other offline smoke, adverse semantic and fixture parity checks passed in that run. Later CI steps were skipped because of the unit-test failure. Exact corrected-revision CI must be checked separately. No production code change needed for the test-helper flaw.

## TS03 portable acceptance record

Base: 3f055fc2bd75d8e7a76964413ab755ebc83b08de. [Corrected TS02 exact CI](https://github.com/mohammadAliKeshavarzSarkar/SEO-Engineering/actions/runs/44461807175) completed successfully. Actual job logs show Python 3.12.3, zlib 1.3, 255 tests passed, two identical builds, 212 source-matched archive files and SHA-256 `078a2d8b799cd1c96a39b79ae952c88f6d18d1e1d799506495e94c1f8a8a76a5` for that base only. Exact archive/source verification and previous relocated research smoke passed. No archive asset published or bytes downloaded here; recorded checksum is from hosted log.

| ID | TS03 finding | Correction / planned verification |
|---|---|---|
| TS03-01 | ZIP integrity did not verify the actual installed copy | Add exact membership/hash comparison for fresh installed directory, reject extra/missing/changed/symlink items |
| TS03-02 | Full filename case collisions were checked but different directory prefixes and normalization aliases could be missed; scalar name duplicates could pass | Reject path component collisions, nonportable reserved names/characters, file/directory conflicts and duplicate scalar names |
| TS03-03 | Relocation smoke ran only research; could miss technical tool imports or changed installation files | Run adverse T10, T11, T12 and research from fresh independent project, assert dispositions, check private output placement, target sentinel and identical before/after installed receipt |
| TS03-04 | Real agent discovery and activation not established | Document verified Cursor/Codex placement references; use existing actual activation procedure; no accessible external runtime session in current context |

Nine new regression methods authored; verify changed-commit CI separately. The install check is for trusted fresh local snapshots; not an installer, signature check, secret scanner, sandbox, cross-platform filesystem proof or external model certification. Declared minimum Python 3.10 not independently tested in this checkpoint; hosted runner 3.12.3 was observed in base. No full content/privacy review, stable distribution, packaging asset publication or provider integration. Runtime activation, final privacy/source review and owner license/distribution decisions remain outstanding.

TS03 first run [44462484459](https://github.com/mohammadAliKeshavarzSarkar/SEO-Engineering/actions/runs/44462484459) failed at import: malformed name regex and duplicate trailing source produced during patch generation. Acceptance-record revision also failed. Correction restores single verifier implementation and literal regex end anchor, without weakening installed-tree checks. Corrected CI pending; actual agent activation still not run.
