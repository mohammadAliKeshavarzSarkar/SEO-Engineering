#!/usr/bin/env python3
"""Review declared Next.js delivery and supplied freshness samples; no network or build."""
import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

METHOD = 'T04-v1'
CACHE_MODELS = {'app_previous', 'app_cache_components', 'pages', 'unknown'}
PURPOSES = {'public', 'excluded', 'protected', 'missing', 'redirect'}
STRATEGIES = {'static', 'isr', 'request_time', 'hybrid', 'unknown'}
FEATURES = {'request_time_data', 'isr', 'runtime_dynamic_paths', 'server_actions',
            'request_dependent_handler', 'next_runtime_redirects_or_rewrites',
            'pages_api_routes', 'default_image_optimizer'}
CAPTURES = {'complete', 'partial', 'failed', 'not_collected'}


def nonempty(v):
    return isinstance(v, str) and bool(v.strip())


def optional_text(v):
    return v is None or nonempty(v)


def bool_or_none(v):
    return v is None or type(v) is bool


def timestamp(v):
    if not isinstance(v, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z', v):
        raise ValueError('timestamp must be UTC YYYY-MM-DDTHH:MM:SSZ')
    return datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)


def unique_object(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise ValueError('duplicate JSON key')
        out[k] = v
    return out


def audit(data):
    json.dumps(data, allow_nan=False)
    if data['schema_version'] != '1' or not nonempty(data['scope']):
        raise ValueError('invalid local QA envelope')
    routes = data['routes']
    if not isinstance(routes, list) or not 1 <= len(routes) <= 500:
        raise ValueError('expected 1–500 route plans')
    seen, sample_ids, results = set(), set(), []
    for row in routes:
        ident = row['id']
        if not nonempty(ident) or ident in seen or not nonempty(row['plan_ref']):
            raise ValueError('unique route ID and plan reference required')
        seen.add(ident)
        major = row['next_major']
        if major is not None and (type(major) is not int or not 1 <= major <= 100):
            raise ValueError('next_major must be integer or null')
        if row['router'] not in ('app','pages','unknown') or row['cache_model'] not in CACHE_MODELS:
            raise ValueError('invalid router or cache model')
        if row['deployment'] not in ('static_export','runtime','unknown') or row['strategy'] not in STRATEGIES:
            raise ValueError('invalid deployment or strategy')
        if row['purpose'] not in PURPOSES or not nonempty(row['expected_context']):
            raise ValueError('invalid route purpose or missing reviewed context')
        features = row['required_features']
        if features is not None and (not isinstance(features,list) or
            any(not isinstance(v,str) or v not in FEATURES for v in features) or len(set(features)) != len(features)):
            raise ValueError('required_features must be known unique features or null')
        statuses = row['expected_statuses']
        if statuses is not None and (not isinstance(statuses,list) or not statuses or
            any(type(v) is not int or not 100 <= v <= 599 for v in statuses) or len(set(statuses)) != len(statuses)):
            raise ValueError('invalid expected statuses')
        target = row['expected_content_revision']
        deadline = row['fresh_by']
        if not optional_text(target) or (target is None) != (deadline is None):
            raise ValueError('freshness needs both reviewed target revision and deadline, or neither')
        due = timestamp(deadline) if deadline is not None else None
        flags, deferred = [], []
        model, router = row['cache_model'],row['router']
        if model == 'unknown' or major is None or router == 'unknown':
            deferred.append('installed_version_router_cache_model_review')
        if ((router == 'app' and model == 'pages') or
            (router == 'pages' and model in ('app_previous','app_cache_components'))):
            flags.append('router_cache_model_conflict_review')
        if model == 'app_cache_components' and major is not None and major < 16:
            flags.append('cache_components_version_compatibility_review')
        if row['deployment'] == 'unknown':
            deferred.append('deployment_capability_unknown')
        if row['deployment'] == 'static_export':
            if row['strategy'] in ('isr','request_time','hybrid'):
                flags.append('static_export_runtime_strategy_conflict_review')
            if features is None:
                deferred.append('static_export_feature_inventory_unknown')
            elif features:
                flags.append('static_export_runtime_features_review')
        if statuses is None:
            deferred.append('intended_http_status_unknown')
        if due is None:
            deferred.append('no_reviewed_freshness_target')
        samples = row['samples']
        if not isinstance(samples,list) or len(samples) > 100:
            raise ValueError('expected at most 100 samples per route')
        if not samples:
            deferred.append('no_response_samples')
        evaluated = []
        for s in samples:
            sid = s['id']
            if not nonempty(sid) or sid in sample_ids or not nonempty(s['context_id']):
                raise ValueError('unique sample ID and context required')
            sample_ids.add(sid)
            state = s['capture_status']
            if state not in CAPTURES or not optional_text(s['content_revision']) or not bool_or_none(s['private_payload_visible']):
                raise ValueError('invalid sample state/value')
            status = s['http_status']
            if status is not None and (type(status) is not int or not 100 <= status <= 599):
                raise ValueError('invalid observed HTTP status')
            ref = s['evidence_ref']
            if state == 'not_collected':
                if ref is not None or s['observed_at'] is not None:
                    raise ValueError('uncollected sample has no capture reference/time')
                when = None
            else:
                if not nonempty(ref):
                    raise ValueError('attempted capture needs evidence reference')
                when = timestamp(s['observed_at'])
            if state in ('failed','not_collected') and any(s[k] is not None for k in
                    ('http_status','content_revision','private_payload_visible')):
                raise ValueError('failed/uncollected sample cannot assert values')
            issues, unknown = [], []
            # Affirmative exposure evidence is an independent escalation even
            # if comparison is otherwise incomplete. Never infer safety from false.
            if s['private_payload_visible'] is True:
                issues.append('suspected_unauthorized_payload_exposure_escalate')
            if s['context_id'] != row['expected_context']:
                unknown.append('sample_context_mismatch')
            if state != 'complete':
                unknown.append('sample_capture_incomplete')
            comparable = not unknown
            freshness = 'not_assessed'
            if comparable:
                if status is None or statuses is None:
                    unknown.append('status_comparison_unavailable')
                elif status not in statuses:
                    issues.append('http_status_differs_from_expectation_review')
                if due is None or s['content_revision'] is None or status != 200:
                    unknown.append('freshness_comparison_unavailable')
                elif s['content_revision'] == target:
                    freshness = 'target_observed'
                elif when < due:
                    freshness = 'different_before_deadline'
                else:
                    freshness = 'different_at_or_after_deadline'
                    issues.append('freshness_target_not_observed_by_deadline_review')
            evaluated.append({'id':sid,'evidence_ref':ref,'observed_at':s['observed_at'],
                              'context_id':s['context_id'],'capture_status':state,
                              'freshness':freshness,'review_findings':issues,'deferred_checks':unknown})
        results.append({'id':ident,'plan_ref':row['plan_ref'],'review_findings':flags,
                        'deferred_checks':deferred,'samples':evaluated})
    return {'method':METHOD,'scope':data['scope'],'routes':results,'review_required':True,
            'limits':'Reviewed declarations and supplied samples only; exact content revision equality is a project-defined assertion, not cache inference. No cache access, invalidation, framework build, live request, authorization or indexing verified.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args = p.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding='utf-8'),object_pairs_hook=unique_object)
        report = audit(data)
        with args.output.open('x',encoding='utf-8') as out:
            json.dump(report,out,indent=2,ensure_ascii=False,allow_nan=False)
            out.write('\n')
    except (OSError,ValueError,KeyError,TypeError,AttributeError) as exc:
        print('Next route QA failed:',exc)
        return 1
    print('Reviewed route plans and supplied samples; manual review required.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
