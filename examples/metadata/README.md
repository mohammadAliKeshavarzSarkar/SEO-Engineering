# T08 synthetic metadata exercise

Hand-authored reviewed fictional facts and capture strings. No actual HTML, deployed markup, content validation or search test. From the library root:

```sh
python3 scripts/audit_metadata.py --input examples/metadata/sample.json --output metadata-report.json
```

Expected: Persian guide produces a draft and matching literal observations; second page flags title/canonical discrepancies and invalid JSON, with uncollected render deferred. Draft is NOT published. See [T08](../../docs/03-technical/t08-metadata-structured-data.md). Exit zero means processed, not eligible for rich results.
