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

The second manifest must report canonical mismatch and missing HTML, with exit code 1. This is an offline smoke test for initial static HTML: declared files, single nonempty title/description/canonical/H1, chosen canonical, simple robots meta exclusions and duplicate title/description policy. These are project conventions, not universal eligibility rules. Mark `indexable:false` to skip a route. It does not check HTTP status, headers, JS rendering, bots, server redirects, sitemap, content quality, search indexing, schema, or performance. The simple parser is not a browser and does not establish effective head placement or bot-specific directive precedence. Document exceptions rather than changing pages blindly. `check_docs.py` checks relative file targets, not external URLs or heading anchors. Both tools are safe offline and require no credentials.

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

From the full trusted repository checkout only, run `python3 scripts/verify_release.py`. Executes unit tests, docs path checks, valid and deliberately failing HTML fixture, five JSON fixture CLIs, package build/extraction checks and fixture output parity. No network or user-provided executable commands. Does not execute behavioral evaluations or verify a real agent installation. Inspect the full output; nonzero exit indicates a required automated check failed. Record human review and other gates separately.
