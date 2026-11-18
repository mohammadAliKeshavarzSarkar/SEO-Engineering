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
