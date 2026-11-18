#!/usr/bin/env python3
"""Compare reviewed local QA observations; not a crawler or shared evidence schema."""
import argparse
import json
from pathlib import Path

METHOD = 'T02-v1'
CAPTURE = {'complete', 'partial', 'failed', 'not_collected'}
CONTENT = {'present', 'partial', 'absent', 'unknown'}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def strings(value):
    return isinstance(value, list) and all(isinstance(v, str) for v in value)


def ids(value):
    return strings(value) and all(nonempty(v) for v in value) and len(value) == len(set(value))


def boolean_or_none(value):
    return value is None or type(value) is bool


def unique_object(pairs):
    data = {}
    for key, value in pairs:
        if key in data:
            raise ValueError('duplicate JSON key')
        data[key] = value
    return data


def capture(row):
    if not isinstance(row, dict) or row['status'] not in CAPTURE:
        raise ValueError('invalid capture status')
    if not nonempty(row['context_id']):
        raise ValueError('capture context ID required')
    ref = row['evidence_ref']
    if row['status'] == 'not_collected':
        if ref is not None:
            raise ValueError('uncollected capture must not assert evidence')
    elif not nonempty(ref):
        raise ValueError('attempted capture requires evidence reference')
    if row['primary_content'] not in CONTENT:
        raise ValueError('invalid primary content state')
    for name in ('titles', 'canonicals'):
        if row[name] is not None and not strings(row[name]):
            raise ValueError('metadata must be string array or null')
    if row['link_targets'] is not None and not ids(row['link_targets']):
        raise ValueError('link target IDs must be unique strings or null')
    if not boolean_or_none(row['meta_noindex']):
        raise ValueError('meta_noindex must be boolean or null')
    if row['status'] in ('failed', 'not_collected') and (
        row['primary_content'] != 'unknown' or any(row[k] is not None for k in
        ('titles', 'canonicals', 'meta_noindex', 'link_targets'))
    ):
        raise ValueError('failed/uncollected capture cannot assert successful values')


def audit(data):
    json.dumps(data, allow_nan=False)
    if data['schema_version'] != '1' or not nonempty(data['scope']):
        raise ValueError('invalid local QA envelope')
    routes = data['routes']
    if not isinstance(routes, list) or not 1 <= len(routes) <= 500:
        raise ValueError('expected 1–500 route pairs')
    seen = set()
    results = []
    for row in routes:
        ident = row['id']
        if not nonempty(ident) or ident in seen:
            raise ValueError('unique nonempty route IDs required')
        seen.add(ident)
        if not boolean_or_none(row['index_intent']) or not boolean_or_none(row['http_noindex']):
            raise ValueError('index intent and HTTP noindex must be boolean or null')
        status = row['http_status']
        if status is not None and (type(status) is not int or not 100 <= status <= 599):
            raise ValueError('invalid HTTP status')
        if status is None and row['http_noindex'] is not None:
            raise ValueError('HTTP directive cannot be known without response')
        if row['comparability'] not in ('matched', 'mismatch', 'unknown'):
            raise ValueError('invalid comparability')
        if row['readiness'] not in ('met', 'not_met', 'unknown'):
            raise ValueError('invalid browser readiness')
        required = row['required_link_targets']
        if required is not None and not ids(required):
            raise ValueError('required target IDs must be unique strings or null')
        src, dom = row['source'], row['rendered']
        capture(src)
        capture(dom)
        if row['comparability'] == 'matched' and src['context_id'] != dom['context_id']:
            raise ValueError('matched comparison has different context IDs')
        if dom['status'] == 'not_collected' and row['readiness'] != 'unknown':
            raise ValueError('uncollected browser readiness must be unknown')
        flags, deferred, compared = [], [], []
        if row['index_intent'] is None:
            deferred.append('index_intent_unknown')
        elif row['index_intent']:
            if status is None:
                deferred.append('initial_http_status_unknown')
            elif status != 200:
                flags.append('intended_public_status_review')
            if row['http_noindex'] is True:
                flags.append('applicable_http_noindex_review')
            elif row['http_noindex'] is None:
                deferred.append('http_directive_unknown')
            if src['meta_noindex'] is True:
                flags.append('initial_meta_noindex_review')
            elif src['meta_noindex'] is None or src['status'] != 'complete':
                deferred.append('initial_meta_directive_incomplete')
        if row['comparability'] != 'matched':
            deferred.append('capture_context_not_established')
        if src['status'] != 'complete':
            deferred.append('source_capture_incomplete')
        if dom['status'] != 'complete':
            deferred.append('rendered_capture_incomplete')
        if row['readiness'] != 'met':
            deferred.append('browser_readiness_not_established')
        ready = (row['comparability'] == 'matched' and src['status'] == 'complete'
                 and dom['status'] == 'complete' and row['readiness'] == 'met' and status == 200)
        if not ready:
            deferred.append('paired_comparison_not_performed')
        else:
            for field in ('titles', 'canonicals', 'meta_noindex', 'link_targets'):
                if src[field] is None or dom[field] is None:
                    deferred.append(field + '_comparison_unavailable')
                    continue
                compared.append(field)
                if field == 'link_targets':
                    if set(src[field]) - set(dom[field]):
                        flags.append('source_link_targets_not_in_render_review')
                    if set(dom[field]) - set(src[field]):
                        flags.append('render_added_link_targets_review')
                elif src[field] != dom[field]:
                    flags.append(field + '_changed_review')
            if src['meta_noindex'] is True and dom['meta_noindex'] is False:
                flags.append('initial_meta_noindex_absent_after_render')
            if row['index_intent'] is True and dom['meta_noindex'] is True:
                flags.append('rendered_meta_noindex_review')
            for label, snapshot in (('source',src), ('rendered',dom)):
                if snapshot['canonicals'] is not None and len(snapshot['canonicals']) > 1:
                    flags.append(label + '_multiple_canonical_declarations_review')
            x, y = src['primary_content'], dom['primary_content']
            if 'unknown' in (x,y):
                deferred.append('primary_content_comparison_unavailable')
            else:
                compared.append('primary_content')
                if x == 'present' and y in ('partial','absent'):
                    flags.append('primary_content_regression_review')
                elif x in ('absent','partial') and y == 'present':
                    flags.append('client_completion_review')
                elif x in ('absent','partial') and y in ('absent','partial'):
                    flags.append('primary_content_incomplete_in_both_review')
            if required is None or dom['link_targets'] is None:
                deferred.append('required_link_target_check_unavailable')
            else:
                compared.append('required_link_targets')
                if set(required) - set(dom['link_targets']):
                    flags.append('required_link_targets_missing_from_render_review')
        results.append({
            'id':ident, 'paired_comparison': 'performed' if ready else 'not_performed',
            'compared_fields':compared, 'review_findings':flags, 'deferred_checks':deferred,
            'source_ref':src['evidence_ref'], 'rendered_ref':dom['evidence_ref'],
            'context_ids':[src['context_id'],dom['context_id']]
        })
    return {'method':METHOD,'scope':data['scope'],'routes':results,'review_required':True,
            'limits':'Reviewed supplied observations only; no browser execution, HTTP verification, bot emulation, index or ranking proof. Findings are review candidates; no findings is not a pass.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding='utf-8'), object_pairs_hook=unique_object)
        report = audit(data)
        with args.output.open('x', encoding='utf-8') as out:
            json.dump(report, out, ensure_ascii=False, indent=2, allow_nan=False)
            out.write('\n')
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        print('Rendering QA input failed:', exc)
        return 1
    print('Rendering observations compared where eligible; review required.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
