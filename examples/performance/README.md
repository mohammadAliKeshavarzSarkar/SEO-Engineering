# T09 synthetic performance evidence

Fictional numbers, not actual measured performance. Run from library root:

```sh
python3 scripts/audit_performance.py --input examples/performance/sample.json --output performance-report.json
```

Expected: origin mobile LCP needs improvement, INP unknown, CLS good; lab LCP median decreases from 3200 to 2300 ms within reviewed tolerance, mismatched profile defers comparison. No origin-to-page substitution, statistical significance, field improvement or ranking result. See [T09](../../docs/03-technical/t09-performance.md).
