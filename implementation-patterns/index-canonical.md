# Index and canonical implementation patterns

Use [T06](../docs/03-technical/t06-indexing-canonicals.md). Synthetic examples, not live modifications.

## A. Retained equivalent variant
A fictional printable rendering of a guide remains useful for users. If actual primary content is equivalent and the guide is intended representative, use the reviewed absolute canonical consistently:
```html
<link rel="canonical" href="https://example.org/guide/">
```
For an equivalent non-HTML resource when appropriate, a response Link header could express that same preference:
```text
Link: <https://example.org/guide/>; rel="canonical"
```
These are alternative mechanisms for appropriate content types. Verify exact target and applicable declarations; avoid conflicts. Do not add a canonical to unrelated content. If variant is permanently retired with a true replacement, approved direct redirect may be appropriate instead. Preserve useful distinct pages and language variants. Self-canonical is a reviewed convention, not required for every eligible URL.

## B. Intended exclusion versus canonical consolidation
For an intentionally public-but-excluded utility, use applicable noindex in header or meta where authorized and accessible to target crawler. Do not add noindex to a duplicate merely to force another URL to be canonical. A blocked page's directive may remain unseen. Protected account/data need authentication/authorization, not robots or noindex. Genuine removed content without replacement uses accurate missing status. Temporary failure is not permanent removal. Verify actual source/header and route purpose.

## C. Evidence timeline and local QA
Fixture: a guide now serves intended canonical; processed evidence was retrieved after release but last crawl was before release. Technical assessment can be current, processed verdict deferred. A different print variant has conflicting HTTP/HTML declarations. Compare:
```sh
python3 scripts/audit_index_evidence.py --input examples/index-evidence/sample.json --output index-evidence-report.json
```
Use actual authorized Search Console indexed evidence separately from live test; indexed-version API is not live or submission. For real acceptance inspect scoped current response, source and ready DOM, target status, content equivalence, sitemap and links, then reviewed later processed record. No guaranteed date; request indexing only where appropriate and authorized; no unsupported general Indexing API use. Preserve rollback and evidence.
