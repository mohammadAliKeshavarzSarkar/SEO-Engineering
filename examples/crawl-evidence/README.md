# T05 supplied crawl evidence exercise

Hand-authored records, not actual crawler output or a shared provider schema. Run from library root:

```sh
python3 scripts/audit_crawl_evidence.py --input examples/crawl-evidence/sample.json --output crawl-evidence-report.json
```

Expected: blocked route review and possible noindex visibility conflict (directive from separate authorized evidence), sitemap redirect review, incomplete discovery deferred, required render resource disallow review. No blocked URL is fetched by this tool. Googlebot is an evaluated-policy label, not a verified request identity. No site-wide coverage, actual robots match or indexing implied. See [T05](../../docs/03-technical/t05-crawling-robots.md).
