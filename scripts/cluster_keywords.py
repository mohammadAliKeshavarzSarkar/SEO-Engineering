#!/usr/bin/env python3
"""Offline candidate clustering; no search collection or page mutations."""
import argparse
import itertools
import json
import math
import unicodedata
from pathlib import Path
from urllib.parse import urlsplit

VERSION = '1.0'
SCOPE = ('market', 'language', 'device', 'engine', 'surface', 'batch')
TASKS = {'learn', 'do', 'compare', 'transact', 'navigate', 'local'}
FA_MAP = str.maketrans('يك٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹', 'یک01234567890123456789')
UNKNOWN = {'', 'unknown', 'mixed', 'unavailable', 'n/a'}


def normalize(query, language=''):
    text = unicodedata.normalize('NFC', query)
    if language.lower().split('-')[0] == 'fa':
        text = text.translate(FA_MAP).replace('\u200c', ' ')
    return unicodedata.normalize('NFC', ' '.join(text.casefold().split()))


def jaccard(a, b):
    union = a | b
    return len(a & b) / len(union) if union else None


def cluster(records, threshold=0.5, min_urls=5):
    if not math.isfinite(threshold) or not 0 < threshold <= 1 or min_urls < 1:
        raise ValueError('threshold must be in (0,1]; min_urls must be positive')
    if not isinstance(records, list) or not 1 <= len(records) <= 200:
        raise ValueError('expected 1–200 query records per batch')
    by_id = {}
    for item in records:
        if not isinstance(item, dict):
            raise ValueError('each record must be an object')
        for key in ('id', 'query', 'intent', *SCOPE):
            if not isinstance(item.get(key, ''), str):
                raise ValueError(f'{key} must be a string')
        ident, raw = item.get('id', ''), item.get('query', '')
        if not ident.strip() or ident in by_id or not raw.strip():
            raise ValueError('nonempty unique id and query required')
        urls = item.get('urls', [])
        if not isinstance(urls, list):
            raise ValueError('urls must be an array')
        for url in urls:
            if not isinstance(url, str) or any(c.isspace() for c in url):
                raise ValueError('urls must be exact HTTP(S) strings without whitespace')
            parts = urlsplit(url)
            if parts.scheme not in ('http', 'https') or not parts.hostname or parts.username or parts.password:
                raise ValueError('expected public HTTP(S) URL without userinfo')
        key = normalize(raw, item.get('language', ''))
        if not key:
            raise ValueError('empty normalized query')
        by_id[ident] = (item, key, set(urls))
    pairs, eligible = [], set()
    ids = sorted(by_id)
    for a, b in itertools.combinations(ids, 2):
        x, nx, ux = by_id[a]
        y, ny, uy = by_id[b]
        reasons = []
        if any(x.get(k, '').strip().lower() in UNKNOWN or
               y.get(k, '').strip().lower() in UNKNOWN or x.get(k) != y.get(k) for k in SCOPE):
            reasons.append('scope_missing_or_different')
        if x.get('intent') not in TASKS or x.get('intent') != y.get('intent'):
            reasons.append('intent_unknown_or_different')
        if x.get('complete') is not True or y.get('complete') is not True or min(len(ux), len(uy)) < min_urls:
            reasons.append('insufficient_comparable_results')
        score = None if reasons else jaccard(ux, uy)
        if not reasons and score < threshold:
            reasons.append('below_overlap_threshold')
        if not reasons:
            eligible.add((a, b))
        pairs.append({'a': a, 'b': b, 'normalized_equal': nx == ny,
                      'jaccard': score, 'shared_urls': None if score is None else len(ux & uy),
                      'status': 'candidate' if not reasons else 'review', 'reasons': reasons})
    # Deterministic greedy complete-link partition, not an optimal clustering solver.
    groups = []
    for ident in ids:
        for group in groups:
            if all(tuple(sorted((ident, member))) in eligible for member in group):
                group.append(ident)
                break
        else:
            groups.append([ident])
    return {'version': VERSION, 'unicode_version': unicodedata.unidata_version,
            'threshold': threshold, 'min_urls': min_urls,
            'queries': [{'id': i, 'raw_query': by_id[i][0]['query'], 'match_key': by_id[i][1]} for i in ids],
            'pairs': pairs, 'candidate_groups': groups, 'status': 'review_required'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--threshold', type=float, default=0.5)
    parser.add_argument('--min-urls', type=int, default=5)
    args = parser.parse_args()
    try:
        records = json.loads(args.input.read_text(encoding='utf-8'))
        report = cluster(records, args.threshold, args.min_urls)
        with args.output.open('x', encoding='utf-8') as handle:
            json.dump(report, handle, ensure_ascii=False, indent=2, allow_nan=False)
            handle.write('\n')
    except (OSError, ValueError, TypeError) as exc:
        print(f'Clustering failed: {exc}')
        return 1
    print(f'{len(report["queries"])} records; {len(report["candidate_groups"])} provisional groups. Review required.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
