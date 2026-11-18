# R09 synthetic locale exercise

All URLs and attributes are fictional supplied manifest values, not live observations. Run:

```sh
python3 scripts/audit_locale_manifest.py --input examples/locale-audit/sample.json --output locale-report.json
```

Use a fresh output path. The paired Persian and English guide representatives share a group and link to both members, including themselves. Expected findings: zero. Remove the English page's return annotation to trigger a set mismatch. Change Persian canonical to English to trigger review. A single-language group with no alternates is valid under this contract.

This strict internal contract expects one representative per approved tag, self-canonical representatives and full alternate sets; Google can process some partial reciprocal sets and same-language duplicate configurations require separate review. The tool does not validate official code lists, parse HTML or XML, fetch URLs, verify language or prove index selection. See [R09](../../docs/02-research/r09-multilingual-search-engineering.md).
