# TS05.4 — Consolidated candidate acceptance checkpoint

**Decision: HOLD.** Internal development review only, not a release candidate label, public package release or license grant. Review checkpoint 2026-11-19.

## Exact identity

- Source commit: `88f23b6d41d26a70afd02aec104befb15d5df402`.
- Version: 0.3.0-dev.12 (development).
- Archive SHA-256: `c56feeea0b3da29f38b05cbe9c9a2af17667d8729fc1eafec26be92c86fe402e` (observed in hosted CI; archive bytes not separately downloaded here).
- [Exact core validation](https://github.com/mohammadAliKeshavarzSarkar/SEO-Engineering/actions/runs/44471127840): all steps passed, 295 tests, 216 source-matched archive files, hosted Python 3.12.3 / zlib 1.3; deterministic build and relocated acceptance succeeded.
- [Machine-readable checkpoint](ts05-candidate-checkpoint.json) captures the specific observed and incomplete gates. It is a historical record, not a moving main alias.

The archive checksum equals the preceding TS05.2 source-reviewed package, but this does not make every source revision interchangeable. The earlier pilot preparation package had SHA-256 0d04d5af3ab512a3c16a8a58fc4c01e795af8fdb233d3aeac470973a13e32ace. If that pilot was preregistered, retain its exact source/config/package. Do not pool results across different packages or claim generalization from a public pilot. No agent execution has been observed.

## Mandatory standalone gates

| Gate | State | Evidence needed to close |
|---|---|---|
| offline tests | observed pass | Exact-revision full offline verification passed (295 unit tests), including documentation and routing checks. |
| archive identity | observed pass | Exact checkout, source-matched archive receipt and bundled development metadata verified in hosted job. Archive contents have not been downloaded independently here. |
| reproducibility | observed pass | Two builds of same inputs identical in tested Python/zlib runtime; not a cross-platform guarantee. |
| relocated installation | observed pass | Fresh extracted directory, synthetic project tool invocation, fixture parity and installation integrity checked; no external coding agent invoked. |
| automated privacy screen | observed pass | Screen executed for all 216 archive and 283 tracked files; 3 and 19 heuristic signals respectively. Pass means accounting completed, not privacy clearance. |
| runtime activation | not run | No actual Cursor or Codex discovery, activation or capability test established for this checkpoint. |
| supported runtime matrix | pending | Python 3.10 declared minimum is not independently verified; other OS/filesystem and external runtime support unestablished. Review actual supported scope and test evidence. |
| pilot behavior | not run | 32 planned sessions, no actual execution or independently reviewed grades. The first pair is a workflow gate, not efficacy evidence. |
| full public behavior | not run | 86 public cases with three repeats per arm, 516 sessions planned; author-visible cases not held-out. |
| held out behavior | not run | Independently authored private tasks, frozen settings, actual matched runs and adjudication not available. |
| manual content privacy | pending | All exact package and current tracked files require human content inspection, contextual/rights review and disposition of heuristic findings; historical exposure review separate. |
| source accuracy | pending | 12 selected claim areas reviewed at preceding commit; broader claim coverage and applicable version verification remain outstanding. |
| ownership and rights | pending | Public repository license unassigned; inventory at 7c16494 covers 279 tracked files and 216 expected archived members, not the current 283-file source revision. Refresh for actual review and verify chain of rights. |
| license and distribution | pending | Owner approval of scope, terms, notices, compatible contribution policy and release channels not recorded. |
| candidate handoff | pending | No release version, actual distributed archive, recipient/scope approval, final reviewed receipt or rollback handoff recorded. |
| owner release approval | pending | No explicit owner decision authorizing promotion for this exact artifact. |

An observed pass on an automated gate is scoped to the method and revision. The privacy screen flagged one archive file (3 patterns) and nine tracked files (19 patterns), not confirmed exposures; zero unscanned files. Passing the screen does not waive human file/content review, source rights or approval. The [rights inventory](ts05-rights-inventory.csv) is bound to the earlier 279-file revision; 283 files were tracked at this checkpoint. Recreate rights and manual privacy inventories for the exact intended source, review history/exposure separately and preserve private decisions.

## Independent optional integration

WebsiteBotScroll interoperability is outside the standalone skill archive and is not required to deliver a correctly scoped standalone candidate. The optional consumer's earlier exact revision 9dca2b674ec09675030b5ab6f206c563663869af passed [interop CI](https://github.com/mohammadAliKeshavarzSarkar/SEO-Engineering/actions/runs/44467221190): 29 tests, 48/48 required differential outcomes, 60/60 profile eligibility checks, 12 eligible test inputs, 6 exploratory matches and 6 exploratory differences. No actual exchange, independent replay, production authorization or provider integration approval. Do not bundle that optional component or advertise it as proven by standalone release. A.2.4 and later adapters, REST and MCP retain separate gates.

## Entry procedure for eventual promotion

1. Freeze scope, exact commit and actual locally verified archive. Identify the supported runtime(s), tool permissions, input/output contracts, Python/OS bounds and release channel. Review intended candidate identity and provenance. Preserve previous installation and rollback package separately.
2. Collect actual external activation and evaluation records, including all failure and not-observable states. Verify artifact bytes with the trial controller; require independent reviewers and held-out task evidence. Evaluate actual package, not solely the rubric-restricted pilot variant. Do not use a model's self-report or fabricated trace as evidence. Record any unsupported runtime, unresolved regression or incomplete comparison.
3. Complete manual source/content/privacy and ownership review of actual files, license compatibility, notices, intended rights and owner-approved distribution channel. Record approved scope privately and do not copy secrets or authorization documents into Git.
4. Prepare a uniquely identified reviewed release candidate with correct version, explicit notices/license if selected and applicable, complete changelog, exact package inventory and reproducible archive. Changes to content/version require fresh receipt and impacted checks; behavioral evidence for altered content needs reviewed applicability or rerun, not automatic transfer. Do not label this dev snapshot 0.3.0-rc.1 yet.
5. Review all required gate evidence with the owner. If a major issue cannot be resolved, hold rather than mark pass by omission. No stable promotion without explicit approval for final exact candidate/version/digest/scope. No automatically created tags, releases, assets or license changes.

## How to check the checkpoint

```sh
python3 scripts/check_candidate_checkpoint.py --record operations/ts05-candidate-checkpoint.json
```

The checker validates the integrity of the *record structure*, gate completeness, scope and held-state semantics. It cannot authenticate CI, prove archive bytes, verify independent reviews or confer permissions. It handles only held development checkpoints; it deliberately refuses promotion decisions. For an actual release use independent verification and `templates/skill-release-review.md` with owner review, not this script. The current gate definition requires all listed standalone gates; the optional exchange is reported separately. No approval token or publication workflow is introduced.

## Next real inputs

- Operator runtime report and actual first pair, followed by public and independent held-out runs.
- Private manual privacy and rights decisions, broader source check and selected supported runtime scope.
- WebsiteBotScroll actual evidence and manifest when producer path is ready.
- Owner approval for license, channel and candidate promotion after gate closure.

No additional development phase can honestly certify these inputs without actual evidence. TS05.4 documentation is prepared; TS05.5 remains held.
