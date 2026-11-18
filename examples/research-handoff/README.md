# Synthetic research handoff

The fixture is fictional. E1 is an observed zero within an invented sample; E2 is unknown and must remain null. D1 is a reviewed fictional decision with evidence and reviewer; D2 remains provisional. No live SEO measurement or real approval exists.

Run from the library root:
```sh
python3 scripts/validate_research.py --input examples/research-handoff/sample.json --output handoff-report.json
```

Expected: two evidence records, two decisions, one provisional ID D2. Change E2 to zero or remove E1 to test failure. Use a new output file each run. The envelope is a lightweight reference layer, not a replacement for detailed R01–R09 records.

See [R10](../../docs/02-research/r10-research-automation-and-validation.md).
