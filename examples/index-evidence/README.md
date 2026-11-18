# T06 synthetic local evidence exercise

Hand-authored records, not real Search Console or crawl results. From the library root:

```sh
python3 scripts/audit_index_evidence.py --input examples/index-evidence/sample.json --output index-evidence-report.json
```

Guide: processed last crawl predates supplied change; no current selected-canonical verdict. Print variant: conflicting source/header targets. Other: partial evidence, missing rendered group and no processed evidence. No live request, search API, content equivalence or actual index assessment. Exit zero means processed. See [T06](../../docs/03-technical/t06-indexing-canonicals.md).
