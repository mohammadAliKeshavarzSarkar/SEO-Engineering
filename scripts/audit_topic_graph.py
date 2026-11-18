#!/usr/bin/env python3
"""Audit a supplied internal-link graph; no crawling or indexing claims."""
import argparse
import json
from collections import deque
from pathlib import Path


def audit(data):
    nodes, entries, links = data['pages'], data['entries'], data['links']
    if not all(isinstance(x, list) for x in (nodes, entries, links)):
        raise ValueError('pages, entries and links must be arrays')
    pages = {}
    for node in nodes:
        ident = node['id']
        if not isinstance(ident, str) or not ident.strip() or ident in pages:
            raise ValueError('page IDs must be unique nonempty strings')
        if node['state'] not in ('public', 'private', 'planned'):
            raise ValueError('invalid page state')
        if type(node['index_intent']) is not bool or type(node['priority']) is not bool:
            raise ValueError('expected boolean index_intent and priority')
        if node['state'] == 'private' and node['index_intent']:
            raise ValueError('private pages cannot have index intent')
        pages[ident] = node
    public = {k for k, p in pages.items() if p['state'] == 'public'}
    if not entries or any(e not in public for e in entries):
        raise ValueError('entry IDs must identify existing public pages')
    adjacency = {k: set() for k in public}
    inbound = {k: set() for k in public}
    issues = set()
    for edge in links:
        source, target, kind = edge['from'], edge['to'], edge['kind']
        if source not in pages or target not in pages:
            raise ValueError('link references unregistered page ID')
        if kind not in ('crawlable', 'interaction_only', 'proposed', 'unknown'):
            raise ValueError('invalid link kind')
        if kind == 'crawlable' and source in public and target in public and source != target:
            adjacency[source].add(target)
            inbound[target].add(source)
        if kind == 'crawlable' and source in public and pages[target]['state'] == 'planned':
            issues.add((source, target, 'observed_link_to_planned_page_review'))
    depth = {e: 0 for e in entries}
    queue = deque(sorted(depth))
    while queue:
        source = queue.popleft()
        for target in sorted(adjacency[source]):
            if target not in depth:
                depth[target] = depth[source] + 1
                queue.append(target)
    rows = []
    for ident in sorted(public):
        p = pages[ident]
        rows.append({'id': ident, 'depth': depth.get(ident),
                     'unique_inbound_sources': len(inbound[ident]),
                     'priority_unreachable': p['priority'] and p['index_intent'] and ident not in depth,
                     'index_intent_no_inbound': p['index_intent'] and ident not in entries and not inbound[ident]})
    return {'scope': 'supplied_graph_only', 'review_required': True,
            'pages': rows, 'issues': [{'from': s, 'to': t, 'reason': r} for s,t,r in sorted(issues)]}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input', required=True, type=Path)
    ap.add_argument('--output', required=True, type=Path)
    args = ap.parse_args()
    try:
        result = audit(json.loads(args.input.read_text(encoding='utf-8')))
        with args.output.open('x', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
            f.write('\n')
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        print(f'Audit failed: {exc}')
        return 1
    print('Graph diagnostics written; review required. No live checks performed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
