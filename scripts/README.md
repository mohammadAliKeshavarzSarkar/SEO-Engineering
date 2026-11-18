# Local checks

Requirements: Python 3.10+; standard library only. Run from repository root:

```sh
python3 scripts/check_docs.py
python3 -m unittest discover -s tests
python3 scripts/audit_html.py --manifest examples/routes.json --root examples/site
```

Intentional failure fixture:

```sh
python3 scripts/audit_html.py --manifest examples/routes-failing.json --root examples/site
```

The second manifest must report canonical mismatch and missing HTML, with exit code 1. This is an offline smoke test for initial static HTML: declared files, single nonempty title/description/canonical/H1, chosen canonical, simple robots meta exclusions and duplicate title/description policy. These are project conventions, not universal eligibility rules. Mark `indexable:false` to skip a route. It does not check HTTP status, headers, JS rendering, bots, server redirects, sitemap, content quality, search indexing, schema, or performance. S05 requires an explicit source head for title, description and canonical; detects misplaced description/canonical; ignores template, SVG, MathML and noscript subtrees for this narrow check. Requires an array manifest, absolute HTTP(S) route URLs without credentials/fragments, and actual JSON booleans for indexable. The parser is not a browser and does not establish effective head placement, visibility, malformed HTML recovery, noscript rendering, HTTP robots headers or bot-specific directive precedence. Review skipped nonindexable entries separately. Document exceptions rather than changing pages blindly. `check_docs.py` checks conventional relative file targets and explicit library resources in the master skill, router and execution contract, including the extracted package entry point. It does not check external URLs, heading anchors, all Markdown constructs or semantic accuracy. Both tools are safe offline and require no credentials.

## R04 candidate clustering

Python standard library only. Run `python3 scripts/cluster_keywords.py --input examples/keyword-clustering/input.json --output candidate-report.json` from the root. Output must not exist. Input JSON array of 1–200 records: unique id, raw query, observed market/language/device/engine/surface, comparable batch ID, R03 intent (learn/do/compare/transact/navigate/local), complete boolean, urls list of unique comparable organic URLs (duplicates ignored). Missing scope, incomplete samples, unknown/mixed intent block grouping. Use only sanitized approved evidence; the script does not verify that supplied scopes, dates, intent or completeness attestations are truthful. Preserve source snapshot IDs separately. Defaults threshold 0.5 and min-urls 5; customize for reviewed cases. Output includes raw queries, match keys, pair reasons, scores when comparable, deterministic greedy candidate groups and review_required. No search API, embeddings, final page assignments, volume sums or site mutations. Exact URL comparison, quadratic pair count, language-specific match keys, no claim of perfect clustering. See [R04](../docs/02-research/r04-keyword-normalization-and-clustering.md).

## R07 observed topic graph diagnostics

Run `python3 scripts/audit_topic_graph.py --input examples/topical-architecture/sample.json --output graph-report.json` from the library root (Python standard library only). Output must not exist. Input: JSON object with pages array (unique nonempty id, state public/private/planned, boolean index_intent and priority), entries array of existing public IDs, links array (from, to, kind crawlable/interaction_only/proposed/unknown). 'Crawlable' here means the supplied observation classifies the link form as crawlable; actual HTTP, robots, redirects, rel attributes, access and canonical/index status must be verified outside the tool. Private nodes cannot have index intent. Existing public nodes, even if intentionally nonindexed, are possible graph paths. Only observed crawlable public-to-public edges count; unique sources deduplicated, self-links ignored. Reports shortest graph depth from chosen entries, no-inbound candidates, unreachable priority pages and review warnings for observed links to planned pages. Unregistered IDs or invalid states fail input validation. Proposed links do not count as observed; output is never a live crawl or proof of indexation. Partial inputs produce partial findings. See [R07](../docs/02-research/r07-content-gaps-and-topical-architecture.md).

## R08 backlog triage and scoring

Run `python3 scripts/prioritize_opportunities.py --input examples/opportunity-prioritization/sample.json --output priority-report.json` (standard library only, new output path). JSON array of records: id, severity P0/P1/P2/P3, status pending/verified, fit eligible/unknown/excluded, risk low/medium/high/unknown, confidence low/medium/high/unknown, impact integer 1–5 or null, effort_days two ordered numbers in 0.25–100000 or null, depends_on list of IDs. Inputs must share a declared objective, horizon and reviewed rubric. The utility validates structure, numeric values, dependency reference/cycles and verified status consistency but trusts evidence and severity attestations. P0 always visible for triage when pending; P1 repair not scored; other lanes distinguish risk review, investigation, excluded, blocked and verified. Eligible P2/P3 growth receives low/mid/high effort-sensitivity scores, not predictions or statistical confidence intervals. Queue ordering is not a schedule; prioritize urgent repair investigations and dependency resolution even if not in repair lane. No network or execution authorization. See [R08](../docs/02-research/r08-opportunity-prioritization.md).

## R09 locale manifest diagnostics

Run `python3 scripts/audit_locale_manifest.py --input examples/locale-audit/sample.json --output locale-report.json` (Python standard library, new output path). JSON object: allowed_tags is a reviewed list of language identifiers, pages contains URL, group, locale, integer status, boolean index_intent, canonical and alternate tag/url pairs. The strict representative contract checks full alternate sets, known same-group targets, self references, duplicate tags, 200 status, intended indexability and self-canonical. Language-only singleton needs no alternates. Narrow tag syntax and an allowlist are not an official code registry. Google may process partial reciprocal sets and legitimate fallback reuse or same-language canonical exceptions; review these manually. Exact URL comparisons require consistent encoding. No live fetch, extraction, language detection, access or index verification. Exit 0 for no findings, 1 for review findings, 2 for handled invalid input or IO failure. See [R09](../docs/02-research/r09-multilingual-search-engineering.md).

## R10 handoff and release verification

Run `python3 scripts/validate_research.py --input examples/research-handoff/sample.json --output handoff-report.json` from repository or bundled library root. Checks envelope schema, provenance fields, date parsing, unknown/null distinctions, unique IDs and decision references. Reviewed decisions need a reviewer and observed/estimated evidence. Structural validation does not confirm truth, authorization or scope alignment. Use a new output path. See [R10](../docs/02-research/r10-research-automation-and-validation.md).

From the full trusted repository checkout only, run `python3 scripts/verify_release.py`. Executes unit tests, docs path checks, valid and deliberately failing HTML fixture, JSON fixture CLIs and local artifact-plan QA, package build/extraction checks and fixture output parity. No network or user-provided executable commands. Does not execute behavioral evaluations or verify a real agent installation. Inspect the full output; nonzero exit indicates a required automated check failed. Record human review and other gates separately.

## S01 packaging reproducibility

The package builder fixes member timestamps, permissions and compression level. Repeated builds of the same included bytes in the same pinned Python/zlib runtime should produce identical ZIP bytes. Use fresh filenames and verify actual byte equality and archive SHA-256 before release. This does not scan secrets inside permitted files. See [stabilization](../docs/08-learning/stabilization.md).

## S02 research input integrity and CI

The R10 handoff validator requires calendar dates in YYYY-MM-DD, rejects non-finite/non-serializable evidence, and rejects duplicate JSON object keys on CLI ingestion. Invalid input fails before the output report is opened. This is a structural safeguard, not proof of factual accuracy. Run `python3 -m unittest discover -s tests -v` and `python3 scripts/verify_release.py` from the trusted checkout. The read-only GitHub Actions workflow runs the verifier and full package byte-reproducibility check on pushes to main or manual dispatch. Review actual run conclusions for the specific commit; a configured workflow is not proof of a pass.

## S03 portable package receipt

Maintainer-only tool from the complete trusted checkout: `python3 scripts/verify_package.py --archive seo-engineering-skill.zip --report package-receipt.json`. Requires a fresh output file. Verifies exact selected paths and bytes, one skill entrypoint, simple frontmatter, and safe member types; emits SHA-256, individual file inventory and runtime details. Record reviewed source commit separately. Does not install, run an agent, attest source trust, check all runtime-specific platform rules or scan every allowed file for secrets. CI tests relocated execution separately. See [portable skill acceptance](../docs/01-foundations/portable-skill-acceptance.md).

## S04 benchmark preparation and aggregation

Maintainer-only `scripts/score_benchmark.py` prepares prompt tasks from a frozen suite/config and aggregates independently reviewed paired grades; no model inference or automated judge. See [benchmark protocol](../evaluations/benchmark-protocol.md) and [grade schema](../evaluations/benchmark-grades.md). Public regression cases are not held-out; the scorer never certifies a release. CI plan preparation uses placeholder metadata and creates no real grades.

## T01 architecture evidence summarizer

`python3 scripts/inspect_architecture.py --input examples/architecture/sample.json --output architecture-report.json` processes a reviewed JSON observation envelope with declared dependency hints and 1–500 route records. It separates observed initial content/client completion from declared generation strategy, flags incomplete content, directive discrepancies, status review and supplied unauthorized visibility. It does not crawl, parse HTML, test access, verify real dependencies or generation modes, or establish index status. Unknowns are null or unknown enums; output is not remediation authorization. Use fresh output names. See [T01](../docs/03-technical/t01-architecture-detection.md). Included in portable package and fixture parity checks.

## T02 paired rendering QA

`python3 scripts/audit_rendering.py --input examples/rendering/sample.json --output rendering-report.json` compares reviewed local source and ready-render observations from matched contexts. Input is the local QA projection described in [T02](../docs/03-technical/t02-javascript-rendering.md), NOT an external crawl contract. It keeps applicable header/meta noindex, title/canonical arrays, primary-content states and reviewed link IDs separate; incomplete captures and unknown fields defer comparisons. Complete paired observations produce review candidates, not crawler/index outcomes. Exit zero means input processed, not absence of issues. Python standard library only; no browser, network, dependency installation or provider integration. New output path required. Fixture included in repository and portable smoke/parity tests.

## T03 local SPA artifact-plan QA

`python3 scripts/audit_spa_build.py --input examples/spa-build/sample.json --root examples/spa-build/artifacts --output spa-build-report.json` checks the explicitly reviewed concrete route-to-file plan against a trusted local root. Regular nonempty file existence only; no source execution, pattern expansion, automatic URL-to-path conversion, real Vite build, metadata or deployment inspection. Flags missing, empty, nonregular files, document path conflicts and inconsistent plan intents; shared SPA shell/error document allowed deliberately, runtime route document deferred. Rejects traversal and symlink components; not a sandbox for concurrently mutable or untrusted filesystems. Review flags and deferred checks; exit zero means processed. See [T03](../docs/03-technical/t03-react-vite-spa.md). Bundled with synthetic fixture; repository/package output parity checked.

## T04 Next.js route-plan and freshness QA

`python3 scripts/audit_next_delivery.py --input examples/next-delivery/sample.json --output next-delivery-report.json` reviews supplied route plans, explicit runtime feature requirements and matched observations of a project-defined content revision and deadline. Does not infer deployed cache model, inspect cache, execute Next builds or perform invalidation. Unknowns, failed/mismatched/partial captures defer checks. Static export conflicts are review candidates. Unauthorized payload observation escalates independently; no access verdict from absence. See [T04](../docs/03-technical/t04-nextjs-hybrid.md) for exact format. Standard library, output must not exist; exit zero means processed. Repository and package fixture parity tested; no provider-specific schema.

## T05 crawl evidence review

`python3 scripts/audit_crawl_evidence.py --input examples/crawl-evidence/sample.json --output crawl-evidence-report.json` reviews supplied scoped observations, not raw robots/sitemap files or live crawl results. Compares reviewed permission, index intent, resource needs, sitemap membership, status/canonical/directive observations and link coverage. Failed/unattempted/excluded response fields must be null; incomplete coverage defers no-inbound claims; counts are supplied records only. A known robots decision requires versioned reviewed policy/reference and crawler token; tool does not verify matching. Exit zero means processed, not healthy. See [T05](../docs/03-technical/t05-crawling-robots.md); standard library, new output path, fixture parity in release checks. No provider-specific contract.

## T06 index and canonical evidence review

`python3 scripts/audit_index_evidence.py --input examples/index-evidence/sample.json --output index-evidence-report.json` reviews supplied intended representative, current status/directives/canonical groups and separately sourced processed inspection evidence. Flags conflicting declarations and chains/cycles in complete supplied records; unknown targets and pre-change inspection recency defer checks. Exact URL comparison only, no normalization, equivalence detection, network, live search inspection or indexing actions. See [T06](../docs/03-technical/t06-indexing-canonicals.md). Standard library, new output path, exit zero means processed, not healthy. Fixture parity in release checks; no provider contract.

## T07 migration plan and trace review

`python3 scripts/audit_migration.py --input examples/migration/sample.json --output migration-report.json` compares explicit reviewed URL mappings and supplied GET transaction prefixes. Flags planned and observed cycles/chains, mismatched redirect type, final URL/status, unconfirmed replacements and scope changes. Partial traces defer terminal comparisons; 304 is not a followed redirect. Literal URL comparisons preserve spelling and parameters. No HTTP requests, network authorization, host config, content equivalence or indexing verified. See [T07](../docs/03-technical/t07-url-migrations.md). Standard library, fresh output path, fixture parity in release checks; exit zero means processed, not healthy.

## T08 metadata draft and observation review

`python3 scripts/audit_metadata.py --input examples/metadata/sample.json --output metadata-report.json` emits draft metadata strings and optional narrow Article/BlogPosting JSON-LD from reviewed supplied facts, including script-context-safe JSON. Compares source and rendered capture strings separately to plan, flags exact discrepancies/repeated declarations and malformed JSON, defers incomplete/unknown/unsupported graph evidence. No HTML parsing, language detection, full JSON-LD expansion, vocabulary validation, feature eligibility, deployment or actual display verified. Output values are drafts; metadata strings still need context-appropriate escaping. See [T08](../docs/03-technical/t08-metadata-structured-data.md). Standard library, fresh output path, release fixture parity. Exit zero means processed.

## T09 field and lab performance review

`python3 scripts/audit_performance.py --input examples/performance/sample.json --output performance-report.json` classifies supplied field p75 values at documented thresholds, preserves actual aggregation/device/window and missing observations, and separately compares matched lab cohorts by median/range and predeclared absolute tolerance. Incomplete, failed, unequal or mismatched lab cohorts defer regression verdict. No measurement, RUM aggregation, PSI assessment reproduction, statistical significance, causal or ranking claim. See [T09](../docs/03-technical/t09-performance.md). Standard library, fresh output path and release fixture parity. Exit zero means processed.

## T10 coordinated technical audit

`python3 scripts/audit_technical.py --input examples/technical-audit/sample.json --artifact-root examples/spa-build/artifacts --output technical-report.json` executes only the existing trusted T01–T09 functions selected by reviewed local inputs; preserves native reports, hashes, review/deferred signals, explicit module states and independently flagged escalation. No network, subprocess, automatic grouping, search measurement or deployment. Optional reviewed groups invoke existing R08. Scope and evidence references not independently verified. See [T10](../docs/03-technical/t10-audit-automation.md) for exact schema/exit behavior. CLI exit 0 means processed without failed module; 2 means report with failed module; 1 means envelope/output failure. Any may still require review; no release permission. Fresh output, trusted root, standard library; repository/package parity checked.

## T11 deployment gate review

`python3 scripts/review_release_gates.py --input examples/deployment-regression/sample.json --output release-gates.json` evaluates a reviewed, project-specific gate manifest. Required checks with missing, stale or failed evidence block readiness; optional gaps remain visible, and supplied confirmed exposure escalates independently. Exit zero means a valid report was generated, not deployment approval; inspect its disposition. No network, CI provider calls, actual testing, release or rollback. Fresh output path, standard library, repository/package fixture parity. See [T11](../docs/03-technical/t11-deployment-regression.md).
