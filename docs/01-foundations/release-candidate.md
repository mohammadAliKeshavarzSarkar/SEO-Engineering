# SEO Engineering 0.2.0-rc.1 — release candidate

Candidate checkpoint: 2026-11-18. This is a versioned **source candidate for controlled evaluation**, not a stable v0.2.0 release, certification, public binary distribution or guarantee of agent performance. Read [machine-readable candidate version](distribution-version.json). The version identifies this intended library snapshot; record its exact Git commit and actual archive SHA-256 separately. Do not treat a version string as proof of origin or release approval. If candidate contents change, pin a new commit and increment the candidate version before redistribution.

## What changed since the initial 0.1.0 foundation

- Ten research modules (R01–R10): business objectives, keyword observations, intent/SERP evidence, normalization/clustering, competitors, page mapping, topical architecture, prioritization, multilingual research, and reproducible research validation.
- Master skill with selective task routing, execution contract, evidence boundaries, decision protocols, implementation patterns, workflows and private project templates.
- Six primary offline SEO utilities: static HTML, candidate clustering, internal-link graph, opportunity backlog, locale manifest and research handoff checks. These work on supplied inputs, not a live crawler or search index.
- Supporting documentation validation, deterministic package builder, exact-source archive verifier, release smoke checks and paired benchmark scorer. The scorer consumes independently reviewed grades and does not invoke models.
- Thirty-eight public development regression scenarios, not held-out evidence. S01–S05 cover structural audit, software and packaging integration, benchmark infrastructure and targeted source corrections.
- Practical route delivery pattern and stronger content privacy review, with no change to real website code or search data.

## Evidence at candidate preparation

The preceding S05 revision 6d7812d179316b13172936657b7603d01c62fe42 has a successful [exact-commit CI run](https://github.com/mohammadAliKeshavarzSarkar/SEO-Engineering/actions/runs/44270480722). All recorded job steps passed: checkout, repository and extracted-package smoke checks, deterministic ZIP builds, source-matched archive receipt, relocated synthetic project and public benchmark plan preparation. S05 recorded 88 software tests and matching source/test blobs. These results are for the preceding revision; require successful candidate-commit CI before using the candidate. No independently graded agent runs, external model activation, actual SEO outcomes or comprehensive privacy/source review have been established. See [stabilization record](../08-learning/stabilization.md).

| Gate | State at preparation |
|---|---|
| Research documentation and targeted corrections | Initial scope written and checked |
| Candidate automated verification | Check exact candidate CI; previous S05 passed |
| Source-matched package and version metadata | Check exact candidate CI and local receipt |
| External agent installation and activation | Not run |
| Independent held-out and paired baseline benchmark | Not run |
| Comprehensive current-source and content privacy review | Pending |
| License and redistribution decision | Owner decision pending; no license assigned |
| Public binary distribution / stable release approval | Pending; do not represent this as stable |

## Reproduce the candidate

From the trusted repository, check out the exact candidate commit identified in the release-candidate handoff, not an unpinned moving branch. Confirm clean status, Python 3.10+ (declared minimum, not a tested compatibility matrix), and runtime versions. Use fresh output paths.

```sh
git rev-parse HEAD
git status --short
python3 --version
python3 scripts/verify_release.py
python3 scripts/build_skill.py --out seo-engineering-0.2.0-rc.1.zip
python3 scripts/verify_package.py --archive seo-engineering-0.2.0-rc.1.zip --report seo-engineering-0.2.0-rc.1-receipt.json
```

The separate receipt gives candidate archive and member SHA-256 digests and runtime information. Record the repository commit with the receipt; it is not a signed attestation. Build a second archive with a new filename in the same pinned runtime, compare bytes, and review actual archive contents using the [privacy review](../08-learning/distribution-privacy-review.md). The CI build checks version metadata in the archive against source, but does not publish a downloadable asset. Do not use a build from a dirty checkout or distribute before review and permission. No license is assigned; public visibility does not grant general reuse rights.

## Controlled installation / first task

For an authorized evaluation after reviewing the contents, extract the entire seo-engineering directory into the target runtime's supported skill directory; for a Codex project this may be .agents/skills/. Follow [installation](skill-installation.md) and [portable acceptance](portable-skill-acceptance.md), and consult current runtime docs. Use a separate synthetic project initially, no production credentials or write permissions. Preserve previous version separately and avoid duplicate skill names.

Ask the agent to explicitly load seo-engineering, identify its library root and version, read the router and execution contract, and perform a bounded read-only audit. Require actual resource references, a harmless fixture tool run, evidence/unknown distinctions, scope and a reviewed plan. Record actual activation, tool access, outputs and limitations. A filesystem smoke test is not an independent model session. For actual evaluation follow the [benchmark protocol](../../evaluations/benchmark-protocol.md).

## Promote or roll back

Stable promotion requires explicit owner acceptance of the [release review](../../templates/skill-release-review.md), exact candidate CI, reviewed archive checksum and content, source accuracy, permission/license decisions, external activation, and independent behavioral evidence. Record failures, blocked checks and candidate version in the release record. Do not publish a stable claim or bypass required gates. If a candidate fails, preserve the reviewed prior installation, correct the library, increment candidate version and rerun affected checks; do not silently replace previously shared archive bytes.
