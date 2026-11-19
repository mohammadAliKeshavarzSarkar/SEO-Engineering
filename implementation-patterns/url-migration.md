# URL migration implementation patterns

Use [T07](../docs/03-technical/t07-url-migrations.md). Synthetic examples; not executable host configuration or live changes.

## A. Reviewed explicit mapping (public GET documents)
| Old URL | Action | Target |
|---|---|---|
| /guide/ | retain | same URL |
| /old-guide/ | permanent 301/308 | /guide/ (equivalent) |
| /catalog/?size=large | permanent | /products/?size=large |
| /retired/ | remove 404/410 | none |
| /unknown-old/ | unknown | review |
Actual mappings must use full reviewed URLs and explicit approved origins. Check true equivalence; do not redirect every unknown path to home. Keep valid variants with separate content/locale. Parameter rules are explicit, not inferred. For temporary maintenance, use appropriate actual response and time-limited behavior, not permanent SEO migration. Method-sensitive actions require independent tests; 307/308 preserve method, 301/302 may convert POST to GET.

## B. HTTP trace expectations (not server code)
```text
GET https://old.example.org/guide/
HTTP 301
Location: https://new.example.org/guide/

GET https://new.example.org/guide/
HTTP 200
```
The approved provider records each transaction, timestamp, raw Location and reviewed resolved target, policy and method. Relative Location needs actual resolution; do not follow an out-of-scope destination. Do not send credentials to other origins. A complete trace differs from a stopped prefix. Test legacy chains, loops, 304, wrong target, missing response and preserved parameters. Prefer explicit reviewed rule tables or vetted host-native configuration; verify precedence and actual behavior before deploying. Never construct an external redirect from untrusted query/header input.

## C. Acceptance and rollback
1. Baseline old/new route registry, content, links, assets, metrics, permissions and host config; review mapping and backups.
2. Test staged target content/status and actual host rules in authorized environment, including UTF-8/encoded reserved characters and repeated/ordered params. Protect staging from unauthorized access.
3. With approval, cut over, verify all important old/new direct GET routes, actual redirects, canonical/hreflang, sitemap, resources, UI and forms (separate method-sensitive checks). For eligible domain changes review ownership, all old-domain variants and authorized Change of Address per T07; retain old origin and redirects.
4. Monitor exact mapped cohorts, technical failures and search/business outcomes separately. Stop on material confirmed wrong destinations, failures or exposure. Coordinate smallest approved rollback, cache and DNS effects, and reverify. Retention and retirement require reviewed evidence.

Run offline fixture:
```sh
python3 scripts/audit_migration.py --input examples/migration/sample.json --output migration-report.json
```
This validates supplied plan and trace continuity only, not server rules, equivalence or real deployment. See T07 sources.
