# T02 synthetic observation exercise

These four pairs are constructed QA inputs, not live observations or WebsiteBotScroll's evidence contract. Context IDs are opaque review labels identifying a matched route/request/deployment/profile, not a hash of the actual capture. The repeated context label in this fictional fixture denotes one environment; each pair is reviewed individually. Run from the library root with a fresh output path:

```sh
python3 scripts/audit_rendering.py --input examples/rendering/sample.json --output rendering-report.json
```

Expected: guide has no review findings in its compared fields; client-completed has client_completion_review; regression has initial meta noindex, canonical change, content regression and required link target review; not-rendered has no paired comparison and explicit deferred checks. Exit 0 means input processed; never treat it as SEO success.

See [T02](../../docs/03-technical/t02-javascript-rendering.md) for the complete local QA contract, capture method and limitations.
