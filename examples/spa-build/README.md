# T03 synthetic artifact inventory

Hand-authored fixture, NOT the output of a real Vite or React Router build. No scripts, network or protected content. The guide has explicit document/data paths, the second article is intentionally absent, the application and missing path share a shell, and catalog is declared runtime. From the library root:

```sh
python3 scripts/audit_spa_build.py --input examples/spa-build/sample.json --root examples/spa-build/artifacts --output spa-build-report.json
```

Expected: guide paths present; article required_artifact_missing; protected shell still needs access verification; missing path fallback status review; runtime document not assessed. Exit zero means processing succeeded, not build/release acceptance. Follow [T03](../../docs/03-technical/t03-react-vite-spa.md) for the local plan semantics and actual deployment checks.
