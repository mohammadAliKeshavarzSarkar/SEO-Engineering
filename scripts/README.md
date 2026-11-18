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
