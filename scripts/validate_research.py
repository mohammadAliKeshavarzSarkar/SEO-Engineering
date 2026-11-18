#!/usr/bin/env python3
"""Validate a research handoff envelope, not source truth or publication approval."""
import argparse
import json
from datetime import date
from pathlib import Path


def validate(data):
    def nonempty(value):
        return isinstance(value, str) and bool(value.strip())

    def index(rows):
        if not isinstance(rows, list):
            raise ValueError('expected array')
        result = {}
        for row in rows:
            ident = row['id']
            if not nonempty(ident) or ident in result:
                raise ValueError('missing or duplicate ID')
            result[ident] = row
        return result

    if data['schema_version'] != '1' or not nonempty(data['scope']):
        raise ValueError('unsupported schema or missing scope')
    evidence = index(data['evidence'])
    decisions = index(data['decisions'])
    for row in evidence.values():
        if row['kind'] not in ('observed', 'estimate', 'hypothesis', 'unknown'):
            raise ValueError('invalid evidence kind')
        if not all(nonempty(row[k]) for k in ('source_ref', 'scope', 'limitations')):
            raise ValueError('missing provenance or limitations')
        date.fromisoformat(row['collected_date'])
        if row['kind'] == 'unknown' and row['value'] is not None:
            raise ValueError('unknown value must be null')
        if row['kind'] != 'unknown' and row['value'] is None:
            raise ValueError('known or hypothesized value missing')
    for row in decisions.values():
        refs = row['evidence_ids']
        if not isinstance(refs, list) or any(not nonempty(r) or r not in evidence for r in refs):
            raise ValueError('unresolved evidence reference')
        if row['status'] not in ('provisional', 'reviewed', 'excluded'):
            raise ValueError('invalid decision status')
        if not all(nonempty(row[k]) for k in ('rationale', 'next_check')):
            raise ValueError('missing rationale or next check')
        if row['status'] == 'reviewed' and (not nonempty(row.get('reviewer')) or not any(
            evidence[r]['kind'] in ('observed', 'estimate') for r in refs
        )):
            raise ValueError('reviewed decision needs reviewer and evidence')
    return {'scope': 'supplied_envelope_only', 'valid_structure': True,
            'evidence_count': len(evidence), 'decision_count': len(decisions),
            'provisional': sorted(i for i,r in decisions.items() if r['status'] == 'provisional'),
            'review_required': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        report = validate(json.loads(args.input.read_text(encoding='utf-8')))
        with args.output.open('x', encoding='utf-8') as f:
            json.dump(report, f, indent=2, allow_nan=False)
            f.write('\n')
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        print(f'Validation failed: {exc}')
        return 1
    print('Envelope structure valid; source truth and approval not verified.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
