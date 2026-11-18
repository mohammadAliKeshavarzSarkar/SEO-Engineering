#!/usr/bin/env python3
"""Offline backlog triage; no authorization, forecasting or site changes."""
import argparse
import json
import math
from pathlib import Path

CONFIDENCE = {'medium': 0.5, 'high': 1.0}
LANES = ['incident', 'repair', 'growth', 'review', 'investigate', 'blocked', 'excluded', 'verified']


def valid_number(value, low, high):
    return type(value) in (int, float) and low <= value <= high and math.isfinite(value)


def prioritize(records):
    if not isinstance(records, list) or not records:
        raise ValueError('expected nonempty array')
    items = {}
    for r in records:
        ident = r['id']
        if not isinstance(ident, str) or not ident.strip() or ident in items:
            raise ValueError('unique nonempty IDs required')
        for key, allowed in [('severity', ('P0','P1','P2','P3')), ('status', ('pending','verified')),
                             ('fit', ('eligible','unknown','excluded')), ('risk', ('low','medium','high','unknown')),
                             ('confidence', ('low','medium','high','unknown'))]:
            if r[key] not in allowed:
                raise ValueError(f'{ident}: invalid {key}')
        deps = r['depends_on']
        if not isinstance(deps, list) or any(not isinstance(d, str) for d in deps) or len(deps) != len(set(deps)):
            raise ValueError(f'{ident}: invalid dependencies')
        if r['severity'] in ('P0','P1') and r['fit'] == 'excluded':
            raise ValueError(f'{ident}: excluded issue conflicts with critical/repair severity')
        impact, effort = r.get('impact'), r.get('effort_days')
        if impact is not None and (type(impact) is not int or not 1 <= impact <= 5):
            raise ValueError(f'{ident}: impact must be integer 1–5 or null')
        if effort is not None and (not isinstance(effort, list) or len(effort) != 2 or
                                  not all(valid_number(v, 0.25, 100000) for v in effort) or effort[0] > effort[1]):
            raise ValueError(f'{ident}: invalid effort range')
        items[ident] = r
    # Validate references and detect cycles by repeatedly removing dependency-free nodes.
    pending = {i:set(r['depends_on']) for i,r in items.items()}
    if any(not ds <= items.keys() for ds in pending.values()):
        raise ValueError('unknown dependency')
    while pending:
        free = {i for i,ds in pending.items() if not ds}
        if not free:
            raise ValueError('dependency cycle')
        pending = {i:ds-free for i,ds in pending.items() if i not in free}
    rows = []
    for i,r in items.items():
        unmet = sorted(d for d in r['depends_on'] if items[d]['status'] != 'verified')
        if r['status'] == 'verified' and (unmet or r['fit'] != 'eligible'):
            raise ValueError(f'{i}: inconsistent verified status')
        reasons = []
        if unmet: reasons.append('unverified_dependencies')
        if r['fit'] == 'unknown': reasons.append('fit_unverified')
        if r['risk'] in ('high','unknown'): reasons.append('risk_review_needed')
        if r['confidence'] not in CONFIDENCE: reasons.append('evidence_review_needed')
        if r['status'] == 'verified': lane = 'verified'
        elif r['severity'] == 'P0': lane = 'incident'
        elif r['fit'] == 'excluded': lane = 'excluded'
        elif unmet: lane = 'blocked'
        elif r['risk'] in ('high','unknown'): lane = 'review'
        elif r['fit'] == 'unknown' or r['confidence'] not in CONFIDENCE: lane = 'investigate'
        elif r['severity'] == 'P1': lane = 'repair'
        elif r.get('impact') is None or r.get('effort_days') is None:
            lane = 'investigate'
            reasons.append('missing_estimate')
        else: lane = 'growth'
        score = None
        if lane == 'growth':
            lo, hi = r['effort_days']
            value = r['impact'] * CONFIDENCE[r['confidence']]
            score = {'low': value/hi, 'high': value/lo, 'mid': value/((lo+hi)/2)}
        rows.append({'id':i, 'severity':r['severity'], 'lane':lane, 'unmet_dependencies':unmet,
                     'reasons':reasons, 'score':score, 'authorization_required':True})
    rows.sort(key=lambda r: (LANES.index(r['lane']), r['severity'] if r['lane'] != 'growth' else '',
                             -r['score']['mid'] if r['score'] else 0, r['id']))
    return {'method':'R08-v1', 'review_required':True, 'rows':rows}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input', required=True, type=Path)
    ap.add_argument('--output', required=True, type=Path)
    args = ap.parse_args()
    try:
        report = prioritize(json.loads(args.input.read_text(encoding='utf-8')))
        with args.output.open('x', encoding='utf-8') as f:
            json.dump(report, f, indent=2, allow_nan=False)
            f.write('\n')
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f'Prioritization failed: {exc}')
        return 1
    print('Review queues written; no execution authorized.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
