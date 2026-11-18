#!/usr/bin/env python3
"""Summarize supplied route-delivery observations; no crawling or code execution."""
import argparse
import json
from pathlib import Path

CONTENT = {'present', 'absent', 'partial', 'unknown'}
EXPECTED = {'public', 'private', 'missing', 'redirect'}
PLANS = {'csr', 'ssg', 'ssr', 'hybrid', 'traditional', 'unknown'}


def text(value):
    return isinstance(value, str) and bool(value.strip())


def unique_object(pairs):
    obj = {}
    for k, v in pairs:
        if k in obj:
            raise ValueError('duplicate JSON key')
        obj[k] = v
    return obj


def summarize(data):
    if data['schema_version'] != '1' or not text(data['scope']):
        raise ValueError('invalid scope/schema')
    packages = data['declared_dependencies']
    if not isinstance(packages, dict) or not all(text(k) and text(v) for k,v in packages.items()):
        raise ValueError('expected dependency name/version strings')
    known = ('react','react-dom','vite','next','vue','nuxt','@angular/core','astro','svelte','@sveltejs/kit')
    hints = [{'package':k,'declared_spec':packages[k]} for k in known if k in packages]
    routes = data['routes']
    if not isinstance(routes, list) or not routes or len(routes) > 500:
        raise ValueError('expected 1–500 route observations')
    seen = set()
    results = []
    for r in routes:
        ident = r['id']
        if not text(ident) or ident in seen or not text(r['evidence_ref']):
            raise ValueError('unique ID and evidence reference required')
        seen.add(ident)
        if r['expected'] not in EXPECTED or r['declared_strategy'] not in PLANS:
            raise ValueError('invalid route expectation or declared strategy')
        for f in ('source_content','rendered_content'):
            if r[f] not in CONTENT:
                raise ValueError('invalid content observation')
        status = r['status']
        if status is not None and (type(status) is not int or not 100 <= status <= 599):
            raise ValueError('status must be HTTP integer or null')
        for f in ('initial_noindex','rendered_noindex','unauthorized_content_visible'):
            if r[f] is not None and type(r[f]) is not bool:
                raise ValueError('directive/access observation must be boolean or null')
        findings = []
        delivery = 'not_assessed'
        if r['expected'] == 'private':
            if r['unauthorized_content_visible'] is True:
                findings.append('suspected_private_content_exposure_escalate')
            elif r['unauthorized_content_visible'] is None:
                findings.append('authorization_unverified')
        elif r['expected'] == 'missing':
            if status is None:
                findings.append('missing_route_status_unknown')
            elif status not in (404,410):
                findings.append('missing_route_status_review')
        elif r['expected'] == 'redirect':
            if status is None:
                findings.append('redirect_status_unknown')
            elif status not in (301,302,303,307,308):
                findings.append('redirect_status_review')
            else:
                findings.append('redirect_destination_not_checked')
        else:
            if status != 200:
                findings.append('public_status_unknown' if status is None else 'public_status_review')
            if r['initial_noindex'] is True:
                findings.append('initial_noindex_review')
                if r['rendered_noindex'] is False:
                    findings.append('initial_noindex_removed_after_render')
            elif r['initial_noindex'] is None:
                findings.append('initial_index_directive_unknown')
            if r['rendered_noindex'] is True:
                findings.append('rendered_noindex_review')
            if status == 200:
                src, dom = r['source_content'], r['rendered_content']
                if src == 'present':
                    delivery = 'initial_content_observed'
                    if dom in ('absent','partial'):
                        findings.append('content_regression_after_render')
                    elif dom == 'unknown':
                        findings.append('rendered_content_unknown')
                elif src in ('absent','partial') and dom == 'present':
                    delivery = 'client_completion_observed'
                    findings.append('evaluate_render_dependency')
                elif src in ('absent','partial') and dom in ('absent','partial'):
                    delivery = 'incomplete_in_both_observations'
                    findings.append('investigate_missing_primary_content')
                else:
                    delivery = 'insufficient_observations'
                    findings.append('collect_source_and_render_evidence')
        results.append({'id':ident,'declared_strategy':r['declared_strategy'],
                        'delivery_observation':delivery,'findings':findings,
                        'evidence_ref':r['evidence_ref']})
    return {'schema_version':'1','scope':data['scope'],'dependency_hints':hints,
            'routes':results,'review_required':True,
            'limits':'Supplied observations only; no framework, actual generation mode, authorization, headers, redirect destination, index or ranking verified.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding='utf-8'),object_pairs_hook=unique_object)
        json.dumps(data,allow_nan=False)
        report = summarize(data)
        with args.output.open('x',encoding='utf-8') as f:
            json.dump(report,f,indent=2,ensure_ascii=False,allow_nan=False)
            f.write('\n')
    except (OSError,ValueError,TypeError,KeyError,AttributeError) as exc:
        print('Architecture input failed:',exc)
        return 1
    print('Route observations summarized; manual review required.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
