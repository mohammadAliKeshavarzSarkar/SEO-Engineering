# TS07.3 — Progressive reference loading

Date 2026-11-19. Base 65d2104992e0e120d5392703b85e31cd2bb74e87. [Prior exact CI](https://github.com/mohammadAliKeshavarzSarkar/SEO-Engineering/actions/runs/44479003801) passed 311 tests, verified 219 archive files and screened 301 tracked files. Archive SHA-256 5fbff07a16e4bf07cfd2f5b634a51f0d01f99135500f437bfbb04e36c488e209; not independently downloaded here.

## Method and findings

Raw unique full-file bytes; exact base Git tree sizes with changed portable file sizes computed from their authored UTF-8 text. Common entry includes master, execution contract and router (23370 bytes); material decisions add foundations and decision overview (7059 bytes). Learn scenarios omit that material bundle for this first-load comparison. All-listed comparator loads all listed resources for the SAME authored route IDs, deduplicated, not all library content or measured prior behavior. Initial reads first listed reference per route, plus explicit workflow for T10/T11/T12 and privacy for ANALYTICS. R02 first reference changed to actual R02 methodology. Later reads are conditional and necessary before consequential decisions. No actual tokenizer, tool call, model, runtime or target data counted. Cases are prior public maintainer examples, not independent evaluations.

| Case | Initial bytes | All-listed bytes | Soft initial budget bytes |
|---|---:|---:|---:|
| Q01 | 26087 | 26087 | 49152 |
| Q02 | 48275 | 64003 | 49152 |
| Q03 | 42599 | 50362 | 49152 |
| Q04 | 48036 | 63636 | 49152 |
| Q05 | 28447 | 28447 | 49152 |
| Q06 | 43615 | 56006 | 49152 |
| Q07 | 65657 | 82563 | 81920 |
| Q08 | 47199 | 51373 | 49152 |
| Q09 | 35210 | 35210 | 49152 |
| Q10 | 44969 | 45340 | 49152 |
| Q11 | 42467 | 47616 | 49152 |
| Q12 | 39429 | 41398 | 81920 |
| Q13 | 32912 | 57068 | 49152 |
| Q14 | 0 | 0 | 0 |
| Q15 | 49698 | 64469 | 49152 |
| Q16 | 64311 | 94945 | 81920 |

14 ordinary in-scope cases (excluding maintainer Q13 and unrelated Q14): initial sum 625999 bytes; all-listed sum 751455 bytes. These are sums across distinct fictional cases, not a single context or measured saving. 1 of 16 authored profiles exceed their stated advisory budget. A full resource's size is not its token count. Actual runtime loads, repeated reads, cached inputs, tool output and sections may differ. The initial plan is deliberately not sufficient for all later decisions.

## Implementation

Router gains explicit staged loading, section-use safeguards and 48/80 KiB soft planning budgets (local editorial choices, not runtime limits). Reasons for necessary extra reads and unresolved dependencies can be recorded. Safety and evidentiary completeness take priority; no truncation to satisfy a byte budget. The maintainer-only `scripts/measure_reference_loading.py --out /private/new-profile.json` computes current exact local file sizes from the known catalogue and authored cases, refuses unrelated/unsafe paths and writes exclusively. It is a measurement utility, not a router/classifier, enforcement mechanism or portable tool. Five regression methods check packaged paths, initial privacy/workflow, R02, scope, budget-overrun visibility and missing paths. The previous benchmark candidate remains frozen; no behavior, actual token savings, privacy/rights approval or stable release claimed. Next TS07.4 dependency and conflict resolution.
