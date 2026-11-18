#!/usr/bin/env python3
"""Review supplied crawl/discovery observations; not a crawler or robots evaluator."""
import argparse
import json
from pathlib import Path

METHOD = 'T05-v1'


def text(v):
    return isinstance(v, str) and bool(v.strip())


def boolean(v):
    return v is None or type(v) is bool


def unique_object(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError('duplicate JSON key')
        out[key] = value
    return out


def audit(data):
    json.dumps(data, allow_nan=False)
    if data['schema_version'] != '1' or not text(data['scope']) or not text(data['crawler_policy']):
        raise ValueError('invalid scope, schema or crawler policy')
    if data['coverage'] not in ('complete_declared_scope', 'partial', 'unknown'):
        raise ValueError('invalid coverage')
    if not text(data['stop_reason']):
        raise ValueError('stop reason required')
    rows = data['urls']
    if not isinstance(rows, list) or not 1 <= len(rows) <= 5000:
        raise ValueError('expected 1–5000 reviewed URL records')
    seen, results = set(), []
    counts = {k: 0 for k in ('observed', 'partial', 'failed', 'not_attempted', 'excluded')}
    for r in rows:
        ident = r['id']
        if not text(ident) or ident in seen:
            raise ValueError('unique URL record ID required')
        seen.add(ident)
        if r['purpose'] not in ('acquisition','utility','protected','missing','redirect','unknown'):
            raise ValueError('invalid purpose')
        for key in ('index_intent','sitemap_member','canonical_self','noindex','critical_resource','inbound_link_observed'):
            if not boolean(r[key]):
                raise ValueError(key + ' must be bool or null')
        state = r['collection']
        if state not in counts:
            raise ValueError('invalid collection status')
        counts[state] += 1
        if r['robots'] not in ('allowed','disallowed','unknown'):
            raise ValueError('invalid supplied robots decision')
        if r['robots'] != 'unknown' and not text(r['robots_ref']):
            raise ValueError('supplied robots decision requires reference')
        if r['robots'] == 'unknown' and r['robots_ref'] is not None and not text(r['robots_ref']):
            raise ValueError('invalid robots reference')
        if r['robots'] != 'unknown' and not text(r['robots_agent']):
            raise ValueError('known decision requires evaluated crawler identity')
        if r['robots_agent'] is not None and not text(r['robots_agent']):
            raise ValueError('invalid crawler identity')
        if r['robots_agent'] is None and r['robots'] != 'unknown':
            raise ValueError('missing crawler identity')
        status = r['http_status']
        if status is not None and (type(status) is not int or not 100 <= status <= 599):
            raise ValueError('invalid HTTP status')
        ref = r['evidence_ref']
        if not text(ref):
            raise ValueError('reviewed record requires evidence reference')
        if state in ('failed','not_attempted','excluded') and any(r[k] is not None for k in ('http_status','noindex','canonical_self')):
            raise ValueError('unobserved response cannot assert status or extraction')
        if status is None and (r['noindex'] is not None or r['canonical_self'] is not None):
            raise ValueError('directive or canonical observation requires response')
        if r['discovery'] is not None and (not isinstance(r['discovery'],list) or
                any(not isinstance(x,str) or x not in ('seed','sitemap','link','registry','log','other') for x in r['discovery']) or
                len(r['discovery']) != len(set(r['discovery']))):
            raise ValueError('invalid discovery sources')
        flags, deferred = [], []
        if r['index_intent'] is True and r['robots'] == 'disallowed':
            flags.append('intended_index_route_disallowed_review')
        if r['critical_resource'] is True and r['robots'] == 'disallowed':
            flags.append('required_render_resource_disallowed_review')
        if r['robots'] == 'unknown':
            deferred.append('robots_decision_unavailable')
        if r['robots'] == 'disallowed' and r['noindex'] is True:
            flags.append('disallow_may_prevent_noindex_discovery_review')
        if r['sitemap_member'] is True:
            if r['purpose'] in ('protected','missing','redirect') or r['index_intent'] is False:
                flags.append('sitemap_intent_conflict_review')
            if r['robots'] == 'disallowed':
                flags.append('sitemap_url_disallowed_review')
            if state == 'observed' and status is not None and status != 200:
                flags.append('sitemap_response_status_review')
            elif state != 'observed' or status is None:
                deferred.append('sitemap_response_unverified')
            if state == 'observed':
                if r['noindex'] is True:
                    flags.append('sitemap_noindex_review')
                if r['canonical_self'] is False:
                    flags.append('sitemap_canonical_preference_review')
                if r['noindex'] is None or r['canonical_self'] is None:
                    deferred.append('sitemap_directive_or_canonical_unknown')
        elif r['sitemap_member'] is None:
            deferred.append('sitemap_membership_unknown')
        if r['index_intent'] is True and r['inbound_link_observed'] is False:
            if data['coverage'] == 'complete_declared_scope':
                flags.append('no_inbound_link_in_declared_scope_review')
            else:
                deferred.append('no_inbound_link_claim_deferred_incomplete_scope')
        if state != 'observed':
            deferred.append('response_collection_incomplete')
        if status == 429 or (status is not None and 500 <= status <= 599):
            flags.append('rate_limit_or_server_availability_review')
        if not flags and not deferred and r['index_intent'] is None:
            deferred.append('project_index_intent_unknown')
        results.append({'id':ident,'collection':state,'robots_agent':r['robots_agent'],
                        'robots_ref':r['robots_ref'],'evidence_ref':ref,
                        'review_findings':flags,'deferred_checks':deferred})
    return {'method':METHOD,'scope':data['scope'],'crawler_policy':data['crawler_policy'],
            'coverage':data['coverage'],'stop_reason':data['stop_reason'],
            'supplied_record_counts':counts,'urls':results,'review_required':True,
            'limits':'Reviewed supplied records only; no robots evaluation, sitemap parsing, fetch, whole-site coverage, verified Googlebot activity or index proof. Counts are input records, not search-engine crawl budget. Absence is scoped to the supplied observation.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    args = p.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding='utf-8'), object_pairs_hook=unique_object)
        report = audit(data)
        with args.output.open('x',encoding='utf-8') as out:
            json.dump(report,out,indent=2,ensure_ascii=False,allow_nan=False)
            out.write('\n')
    except (OSError,ValueError,TypeError,KeyError,AttributeError) as exc:
        print('Crawl evidence review failed:',exc)
        return 1
    print('Supplied evidence processed; review findings and deferred checks.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
