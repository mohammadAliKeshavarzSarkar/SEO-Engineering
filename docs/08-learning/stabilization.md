# v0.2.0 stabilization and release readiness

Status: development candidate; not released or behaviorally certified. S01 checkpoint: 2026-11-18.

## Roadmap

| ID | Stage | Exit evidence | State |
|---|---|---|---|
| S01 | Repository quality audit | Inventory, reference scan, targeted fixes and regressions, explicit limits | Initial structural audit and targeted fixes complete; wider semantic review remains |
| S02 | Full automated testing | Actual complete checkout, unit test and utility fixture outcomes; fix and rerun failures | Pending |
| S03 | Portable skill validation | Build twice in pinned runtime, compare checksums, inspect archive, run extracted fixtures and reference checks | Pending full integration |
| S04 | Agent behavioral benchmarking | Matched baseline and skill runs, independent grading, held-out cases, actual failure records | Pending |
| S05 | Corrections and improvements | Regressions, reviewed source and privacy checks, reruns for affected gates | Pending |
| S06 | v0.2.0 release | Explicit owner review and release decision, source commit and package checksum, all required checks | Not released |

## S01 audit scope and results

Audited base commit ee2508e016b361259c0f5c7415bdac9b8f708da8 of this repository only, via the GitHub connector. Complete tree listing, 132 tracked files. Connector-based scan resolved 224 conventional relative Markdown link targets across all 80 Markdown files; none missing in the repository or expected portable layout. All 68 distinct library resource paths in the task router exist and are covered by the builder's expected inclusion rules. The projected archive from that base contains 115 files, not an actual built archive. The scan checks relative file paths, not anchors, external URL health, all Markdown constructs, semantic accuracy, or content-level privacy. No unrelated repositories or private project workspace were inspected. Full checkout download was blocked by DNS/network access; the local directory was not a current complete checkout.

## Findings and fixes

| ID | Finding | Correction | Verification |
|---|---|---|---|
| S01-01 | Existing check_docs.py only recognized conventional Markdown links, missing plain router resource paths | Validate explicit library paths in SKILL.md, router and execution contract | Seven targeted checker tests cover both layouts, missing files, unsafe outward links and external/fenced link handling |
| S01-02 | Extracted package checker scanned library subtree but omitted master skill and sibling reference entry points | Include entry-point and top-level reference Markdown in portable mode; check required files | Included in the seven checker tests |
| S01-03 | ZIP timestamps depended on build time, making byte reproducibility unreliable | Fixed ZIP member timestamps, permissions and compression level | Five package-builder tests including identical output from repeated builds in a pinned runtime |
| S01-04 | Full release and behavioral verification are not established by published test files | Keep release gates and status explicit; require actual evidence | Still pending full checkout, package integration and independent agent runs |

Targeted local tests: 12/12 pass on Python 3.13.5 with synthetic temporary file trees (no live site). Eight of these test cases are new (seven docs checks, one reproducibility regression). The four changed Python source/test blobs were checked against the locally tested Git blob hashes. This is not a full-suite run, actual full archive build, external-runtime installation, content-level secret audit or comprehensive source fact check. No claim of model improvement or SEO outcome.

## S02/S03 execution contract

From a complete trusted checkout pinned to the reviewed candidate, run:
```sh
python3 scripts/check_docs.py
python3 -m unittest discover -s tests -v
python3 scripts/verify_release.py
python3 scripts/build_skill.py --out skill-a.zip
python3 scripts/build_skill.py --out skill-b.zip
python3 -c "from pathlib import Path; import hashlib; a,b=[Path(n).read_bytes() for n in ('skill-a.zip','skill-b.zip')]; assert a==b; print(hashlib.sha256(a).hexdigest())"
```
Use fresh output names. Record Python/zlib versions, commit, output and exit codes. Identical bytes are expected for identical inputs within a pinned runtime; do not claim identical compression across arbitrary Python/zlib versions. Review archive membership and actual contents for private data before distribution. Repository tests and package fixture results are separate from external installation and behavioral evaluation. See [release review](../../templates/skill-release-review.md) and [behavioral protocol](../../evaluations/README.md). Record failures and do not silently skip missing gates.

## Wider quality review still needed

Revalidate change-sensitive platform claims against current primary sources, inspect cross-module terminology and precedence for semantic conflicts, consider stronger malformed-input and fixture-semantic assertions, review privacy boundaries including content inside allowlisted directories, and conduct independent model evaluation. Do not infer these reviews passed from an inventory or source-path check. A released skill provides procedural context, not training or guaranteed rankings.
