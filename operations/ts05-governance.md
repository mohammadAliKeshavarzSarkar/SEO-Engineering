# TS05.3 — Ownership, licensing and distribution decision framework

Review date 2026-11-19. Governance proposal and inventory, not a license, legal opinion, grant of rights or release approval.

## Observed starting point

GitHub reports public visibility and no assigned repository license. No owner authority or chain-of-title review has been completed. The repository account/controller is not proof of copyright ownership. GitHub public visibility allows viewing and forking through the service, not an unrestricted additional commercial-use or redistribution grant. Making the repository private later does not recall existing copies or detached public forks. Do not change visibility, rewrite history, add a LICENSE, assert copyright ownership or publish a package without owner authorization.

The latest source-reviewed checkpoint is 7c1649419205fccc69a568d69fc49d8cb5c11558. [CI](https://github.com/mohammadAliKeshavarzSarkar/SEO-Engineering/actions/runs/44470498445) passed 295 tests, 216 source-matched archive files, 279 tracked files scanned. Archive SHA-256 from hosted log: c56feeea0b3da29f38b05cbe9c9a2af17667d8729fc1eafec26be92c86fe402e. One archived file / three signals, nine tracked files / nineteen signals remain review leads, not confirmed exposures. The archive has not been downloaded here. No actual owner approval or behavioral evaluation.

## Rights boundaries and actual inventory

The [rights inventory](ts05-rights-inventory.csv) enumerates all 279 file paths and Git blob OIDs at that exact source commit, with 216 expected archive members derived from the inspected builder allowlist; counts match hosted CI. It is a source-tree inventory, not an independent archive-byte receipt or legal finding. Git object IDs identify source blobs, not SHA-256 content hashes. All records are pending review. New or modified files require a refreshed inventory; this file intentionally records a historical base, not itself or subsequent changes.

| Review group | Tracked files | Expected archive members |
|---|---:|---:|
| maintainer_operations | 7 | 0 |
| knowledge_documentation_configuration | 148 | 141 |
| examples_tests_evaluations | 83 | 56 |
| optional_interoperability | 14 | 0 |
| software | 27 | 19 |

For each group, identify rights holder, original/third-party/AI-assisted provenance, evidence of permission (including employer/client arrangements where applicable), exact license/version and obligations, actual content, notices, review status and permitted channels. Use private review records keyed by source commit, path, blob OID and actual archive receipt; no customer names, contracts or secrets in public CSV.

- Code and scripts: inspect original implementation and copied snippets; review contributor/employment authority, notices, dependency compatibility and generated content origin. Do not assume a repository account owns all code.
- Skill prompts, guidance, workflows, templates: independently assess authored text, source paraphrase and quoted third-party material. Referencing official docs does not license the docs themselves.
- Examples, cases and fixtures: verify synthetic provenance and rights, or explicit approval for actual material. Data consent and publication authorization separate from copyright.
- Optional interoperability: preserve upstream ownership. The canonical WebsiteBotScroll schema and fixture bytes are not vendored in the portable archive. Contract acceptance and private exchange are not blanket redistribution rights or a license. Review [declared optional dependency inventory](ts05-dependency-rights.json) at exact installed versions, provenance and notices; it is not a complete SBOM. Core portable utilities use standard-library dependencies; Python itself is not bundled.
- Brand, names and logos: do not assume copyright permissions grant trademark usage or endorsement. Keep private project intelligence out of source, package, issues and logs. Third-party permissions may be narrower than chosen project license.

## Owner choices (not adopted)

| Distribution direction | Candidate policy | Implications |
|---|---|---|
| Internal toolkit | Owner-approved internal reuse; private controlled access | Retain reusable asset internally; existing public copies remain outside access revocation |
| Open reusable software | MIT for authorized code and expressly included documentation | Broad reuse, including commercial reuse, with notices retained |
| Open reusable software with explicit patent terms | Apache-2.0 for expressly scoped authorized work | Broad reuse and patent grant with redistribution/notice obligations |
| Split open code and documentation | MIT or Apache-2.0 for code; separately scoped documentation license such as CC BY 4.0 | Make per-path treatment explicit, review compatibility and avoid ambiguity for mixed skill/prompt files |
| Commercial or negotiated reuse | Owner-approved bespoke terms with legal review | Define intended recipients and rights; do not describe restricted terms as open source |

Recommendation for this development stage: retain unassigned licensing until chain of title, third-party rights, privacy and intended commercial reuse are resolved. For widespread reuse of an eventual genuinely open toolkit, a single permissive license covering clearly authorized code and documentation is easier to maintain than a split license across tightly coupled resources. This is a proposal only; if controlled commercial access is the goal, review repository visibility separately. No license has been selected here.

Standard source references checked 2026-11-19: [GitHub licensing guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository), [GitHub terms](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service), [MIT text](https://opensource.org/license/mit), [Apache-2.0 text](https://www.apache.org/licenses/LICENSE-2.0), [Creative Commons FAQ](https://creativecommons.org/faq/), [SPDX identifiers](https://spdx.org/licenses/), [semantic versioning](https://semver.org/). Consult appropriate legal counsel for ownership, applicable exceptions and bespoke terms.

## Proposed distribution channels and compatibility

1. Development: public source visibility is the current observation, not additional license permission. Development archive is local verification material, not published binary.
2. Controlled evaluation: authorization, privacy/rights and specific scope before sharing or installing; pin source commit + exact archive SHA-256; use synthetic data, no production access. Existing preregistered pilot remains immutable. No silent replacement.
3. Candidate: owner approves version and distribution scope; candidate receives a unique version and immutable checksum, release notes, reviewed license text and applicable notices included in package. The current builder does not include root LICENSE/NOTICE automatically; explicitly adapt and test both archive and installed receipts after approval. Do not put license data in a package before decision.
4. Stable: only after exact-candidate software validation, runtime activation, real behavioral evaluation, full privacy/source/rights reviews and owner approval. Record unsupported runtime/platforms, not-tested conditions and rollback steps. The initial interoperability contract version is separate from the skill version; actual exchange and adapter readiness are independently gated. Do not represent optional integration as certified; exclude it from standalone distribution.

Proposed SemVer-style policy: development 0.x is not a stable public API. Define supported CLI names, local JSON schema versions and outputs, skill entrypoint and documented compatibility scope per candidate. Record breaking input/output changes and migration guidance, no silent compatibility fallback. Use unique prerelease labels for intentionally handed-off changed content; never replace a released artifact at the same version. Existing 0.3.0-dev.12 snapshots differ by commit + checksum; no externally published release is asserted. Maintain changelog, exact receipt and rollback record. Preserve previous source candidate; if release fails, hold distribution, record disposition, issue a corrected new version after review rather than overwrite archive/history. No guarantees of rankings or customer outcomes.

## Contributions and maintenance

Proposed contribution path: small reviewed changes, independent source and evidence checks, declared authorship/permission and AI-assisted provenance where appropriate, no customer material or copied unapproved third-party content. Do not merge a contribution that cannot establish permission for the intended distribution; no automatic contributor license agreement or DCO attestation added. Do not assume a PR automatically transfers ownership. Once owner license decision is effective, require compatible contribution terms and notices, and review exact changes before publication. Keep external pull requests, issues and traces free of private evidence. Security reports: contact an authorized maintainer privately using an agreed channel; do not publish exploit details or secrets before triage. No channel or response SLA invented.

## Required owner decision

Use a private copy of [owner decision record](ts05-owner-decision.example.json). Confirm legal rights holder/authority, intended access and commercial policy, treatment of code/documentation/fixtures, third-party permissions and notices, contributor terms, version/compatibility policy and permitted distribution channel. This example is intentionally pending with unset license fields, no approval. Evidence of permission, reviewer findings and actual signed/recorded decisions remain private. Never treat completing an example record as an automated grant of rights.

TS05.4 can prepare a consolidated candidate evidence ledger while rights decisions remain open. TS05.5 remains held. No license, visibility change, new release tag, GitHub release or archive publication in this checkpoint.
