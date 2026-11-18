# T10 composite offline audit

Copies of the nine existing synthetic module inputs, not a unified real website or provider schema. Route identifiers can overlap across modules without denoting the same page. Run at library root:

```sh
python3 scripts/audit_technical.py --input examples/technical-audit/sample.json --artifact-root examples/spa-build/artifacts --output technical-report.json
```

All nine utilities should process; native reports and review/deferred signals retained. T03 uses the existing explicitly trusted synthetic artifact root. No group or priority is assigned automatically. Inspect the report, review relevant signals against their native reports and underlying evidence, then put reviewed groups referencing exact emitted signal IDs in a separate copy of the manifest and rerun with a new output. Unit tests exercise R08 grouping with reviewed synthetic values. Omit the artifact root to see T03 blocked. No live audit, actual site coverage, automatic diagnosis or release approval. See [T10](../../docs/03-technical/t10-audit-automation.md).
