# R07 synthetic graph and content exercise

Everything here is fictional, not a live site or crawl. The [input](sample.json) specifies a home entry, useful hub and guide, an orphan candidate available only via an interaction-only link from home or a link from a private page, a disconnected pair, a private page and a proposed page.

Run from repository root (or bundled library root):
```sh
python3 scripts/audit_topic_graph.py --input examples/topical-architecture/sample.json --output graph-report.json
```
Use a new output path. Expected: home depth 0, hub 1, guide 2 and one unique inbound source despite two links; orphan depth null and no observed public crawlable inbound; island depth null despite one inbound source; island2 also unreachable but not priority; private and planned excluded. No live crawl/indexing conclusion. Graph assumes supplied public state and link types; verify actual HTTP and rendered links separately.

Fictional office furniture coverage: existing usable chair category + selection guide. Support sizing instructions need verified product dimensions and an owner; prefer improving a useful guide before new content. A separate verified fit tool may merit proposal if independently useful. No need to create a pillar for every keyword or delete low-traffic assembly instructions. Add relevant contextual links to verified destinations, not all-to-all footer links. A private dashboard is never exposed to satisfy a graph metric.

See [R07](../../docs/02-research/r07-content-gaps-and-topical-architecture.md) and [decision protocol](../../decision-engine/topical-architecture.md).
