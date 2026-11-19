# TS09.1 — Operational readiness baseline

Date 2026-11-19. **HOLD**. Review source `a931f6fde2ecce1d551a8a1e52134049f77b74ac`; [exact CI](https://github.com/mohammadAliKeshavarzSarkar/SEO-Engineering/actions/runs/44487898347) completed successfully. TS08 is complete as an offline practice phase. This review is a capability and evidence inventory, not an exhaustive code, source, license, privacy or security audit.

## Evidence at the reviewed commit

Version 0.3.0-dev.12; hosted Linux Python 3.12.3, zlib 1.3; 356 passing tests, 284 verified archive members, 389 tracked files screened. Archive SHA-256 `dc2943c5ae42924cb30d3fb6a2e57d9bcb2a5967bbcdc88ef047ba82ba22f760`. Archive not independently downloaded here. Two same-runtime builds matched, verification checked exact source, selected relocated tests retained original skill bytes/target sentinel. CI explicitly staged 32 planned pilot slots and two workspaces, no model execution. Current Git tree: 59 docs files, 30 Python scripts in scripts/, 40 test modules, 107 example files. These counts measure inventory, not effectiveness. Verified historical TS05 job 44471127840 also logged Python 3.12.3 and zlib 1.3; no correction of that frozen record required.

| Capability | Evidence and limits |
|---|---|
| Research R01–R10, technical T01–T12, content, localization, measurement | Authored methods and native offline diagnostics; selected TS06 source reviews, not all factual claims or provider operations verified |
| Skill routing and decision quality TS07 | 37 route families, structural regressions and authored examples; no actual model routing, context savings or response quality measurement |
| TS08 P01–P05 | Source CI executed the offline regression tests, including real disposable three-file patch in P05; no live framework builds, search outcomes or customer tests |
| Packaging and relocation | Same-runtime deterministic archive and selected relocated fixture checks; no external agent discovery or activation |
| WebsiteBotScroll | Separate optional integration with historical synthetic differential tests; actual authorized producer export/replay not received; REST/MCP deferred |
| Behavioral evaluation | Controller, staged rubric-restricted pair and incomplete-run review path exist; actual independent execution and scoring not received |

## Current gates

The [held checkpoint](ts09-readiness-checkpoint.json) reuses the existing TS05 gate vocabulary. Five of 16 mandatory gates have scoped observed passes (offline tests, identity, reproducibility, relocated installation, automated pre-screen). Eleven stay open: activation, supported matrix, pilot, full public benchmark, held-out benchmark, manual privacy, comprehensive source review, rights, license/distribution, handoff and owner approval. Optional exchange stays separate. Not a maturity percentage. Historical [TS05 checkpoint](ts05-candidate-checkpoint.json) is unchanged. No test candidate substitution, release label change, tag, public archive, visibility or license action.

Run the existing structure checker:
~~~sh
python3 scripts/check_candidate_checkpoint.py --record operations/ts09-readiness-checkpoint.json
~~~
It checks record structure only; evidence authenticity is not verified by it.

## Refreshed rights inventory

Public repo metadata license null. No root LICENSE/COPYING/NOTICE in reviewed tree. The earlier rights inventory of 279 files was pinned to 7c1649419205fccc69a568d69fc49d8cb5c11558. Source tree comparison by path and blob OID: 110 added, 54 modified, 225 unchanged, zero deleted. Relative to the frozen 283-file TS05 checkpoint: 106 added, 53 modified, 230 unchanged, zero deleted. The [refreshed inventory](ts09-rights-inventory.csv) covers all 389 reviewed paths; 284 expected archive paths derived from inspected builder allowlist and matched observed CI count. It records Git blob OIDs, not SHA-256 or actual archive bytes. Each row remains pending, including unchanged files. The inventory deliberately excludes this later review commit's new/modified files; refresh again for any new candidate. No ownership proof, dependency license audit or permission grant. Review private evidence with actual owner. One flagged archive file/3 signals, nine flagged tracked files/19 signals, zero unscanned are automated leads, not confirmed leaks or clearance.

## Readiness correction made after baseline

P05 was executed in source CI but not in the extracted-library project smoke. Extend the existing relocated job to execute the packaged capstone from the installed library and check actual receipt and hold state, with installation/target integrity checks retained. Two additional tests check the held baseline structure and refreshed inventory mapping. New CI must pass before claiming relocated P05 coverage. No change to portable resources, diagnostic interfaces, historical benchmark or target. Archive payload expected unchanged, but digest must be confirmed on new exact revision.

## Next steps by evidence dependency

| Phase | Closure evidence |
|---|---|
| TS09.2 | Operator selects one actual supported runtime, exact clean commit and archive/installed receipts; verifies isolation and activation with unscored disposable probes. This review environment has no codex, cursor-agent or agent executable on PATH. Do not assume the operator machine is identical. |
| TS09.3 | Verify intended runtime/OS/Python matrix and exact discovery paths with actual runtime version evidence; use current official runtime docs when executing. Explicitly narrow unsupported scope. |
| TS09.4 | Approved paired pilot, matched configuration and task context; real response and traces in private storage; independent blind and incomplete-session review. No paid inference without explicit consent. First pair before remaining 30. |
| TS09.5 | Only observed defects justify targeted revisions; preserve prior candidate, freeze new identity and rerun affected comparisons without overfitting public cases. |
| TS09.6 | Complete source, rights, privacy and owner decisions for exact artifact; no stable release until required evidence and approval. |

Use [operator procedure](ts04-runtime-launch.md), [incomplete-run review](ts07-instruction-evaluation.md) and [governance](ts05-governance.md) instead of building parallel tooling. Current practical blocker is access to an actual isolated agent runtime and authorized inference; only readiness preparation was possible here. Do not use the repo review as proof of skill efficacy.
