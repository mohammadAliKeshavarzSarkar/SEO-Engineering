# T07 synthetic migration map and HTTP traces

Hand-authored evidence, not live HTTP requests. Run from library root:

```sh
python3 scripts/audit_migration.py --input examples/migration/sample.json --output migration-report.json
```

Expected: guide has no discrepancy in supplied trace; catalog destination loses reviewed query and is flagged; partial trace defers terminal checks; retired route returns intended 410. No URL normalization, network collection or search performance proof. Exit zero means processed. See [T07](../../docs/03-technical/t07-url-migrations.md).
