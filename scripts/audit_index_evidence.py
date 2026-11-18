#!/usr/bin/env python3
"""Review supplied indexing and canonical observations; never query a search index."""
import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit

METHOD = 'T06-v1'


def text(v):
    return isinstance(v, str) and bool(v.strip())


def url(v):
    if not text(v) or any(c.isspace() or ord(c) < 32 for c in v) or '#' in v or '\\' in v:
        return False
    try:
        p = urlsplit(v)
        _ = p.port
        return p.scheme in ('http','https') and bool(p.hostname) and p.username is None and p.password is None
    except ValueError:
        return False


def time(v):
    if not isinstance(v,str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z',v):
        raise ValueError('expected UTC timestamp')
    return datetime.strptime(v,'%Y-%m-%dT%H:%M:%SZ')


def unique_object(pairs):
    out = {}
    for k,v in pairs:
        if k in out:
            raise ValueError('duplicate JSON key')
        out[k] = v
    return out


def audit(data):
    json.dumps(data,allow_nan=False)
    if data['schema_version'] != '1' or not text(data['scope']):
        raise ValueError('invalid local QA envelope')
    rows = data['urls']
    if not isinstance(rows,list) or not 1 <= len(rows) <= 5000:
        raise ValueError('expected 1–5000 URL records')
    by_url, results, edges = {}, [], {}
    seen = set()
    for r in rows:
        ident, u = r['id'],r['url']
        if not text(ident) or ident in seen or not url(u) or u in by_url:
            raise ValueError('unique ID and absolute URL required')
        seen.add(ident)
        by_url[u] = r
        if r['intent'] not in ('representative','duplicate','excluded','protected','unknown'):
            raise ValueError('invalid project intent')
        expected = r['preferred_url']
        if expected is not None and not url(expected):
            raise ValueError('invalid preferred URL')
        if r['intent'] == 'representative' and expected not in (u,None):
            raise ValueError('representative preference must be self or unknown')
        current = r['current']
        state = current['status']
        if state not in ('complete','partial','failed','not_collected'):
            raise ValueError('invalid current observation state')
        if state == 'not_collected':
            if current['evidence_ref'] is not None or current['observed_at'] is not None:
                raise ValueError('uncollected observation has no reference/time')
        else:
            if not text(current['evidence_ref']):
                raise ValueError('attempted observation requires reference')
            time(current['observed_at'])
        status = current['http_status']
        if status is not None and (type(status) is not int or not 100 <= status <= 599):
            raise ValueError('invalid HTTP status')
        for k in ('http_noindex','initial_noindex','rendered_noindex','sitemap_member'):
            if current[k] is not None and type(current[k]) is not bool:
                raise ValueError('expected bool or null')
        if current['robots'] not in ('allowed','disallowed','unknown'):
            raise ValueError('invalid reviewed robots decision')
        fields = ('source_canonicals','header_canonicals','rendered_canonicals')
        for k in fields:
            values = current[k]
            if values is not None and (not isinstance(values,list) or len(values)>100 or not all(url(v) for v in values)):
                raise ValueError('canonical group must contain resolved reviewed absolute URLs or null')
        if state in ('failed','not_collected') and any(current[k] is not None for k in
                ('http_status','http_noindex','initial_noindex','rendered_noindex',*fields)):
            raise ValueError('unobserved response cannot assert values')
        if status is None and any(current[k] is not None for k in
                ('http_noindex','initial_noindex','rendered_noindex',*fields)):
            raise ValueError('response-derived values need HTTP status')
        inspected = r['processed']
        if inspected is not None:
            if not text(inspected['evidence_ref']) or not text(inspected['property']):
                raise ValueError('processed evidence needs property and reference')
            when = time(inspected['retrieved_at'])
            last = inspected['last_crawl_at']
            if last is not None and time(last)>when:
                raise ValueError('crawl cannot follow retrieval')
            if inspected['state'] not in ('indexed','not_indexed','unknown'):
                raise ValueError('invalid reviewed processed state')
            for k in ('user_canonical','selected_canonical'):
                if inspected[k] is not None and not url(inspected[k]):
                    raise ValueError('invalid processed canonical')
        changed = r['changed_at']
        if changed is not None:
            time(changed)
        flags, deferred = [], []
        if r['intent'] == 'representative':
            if current['robots']=='disallowed':
                flags.append('intended_representative_robots_blocked_review')
            elif current['robots']=='unknown':
                deferred.append('robots_unknown')
            if any(current[k] is True for k in ('http_noindex','initial_noindex','rendered_noindex')):
                flags.append('intended_representative_noindex_review')
            if state=='complete' and status is not None and status!=200:
                flags.append('intended_representative_status_review')
            if current['sitemap_member'] is False:
                flags.append('representative_sitemap_omission_review')
        elif r['intent'] in ('duplicate','excluded','protected') and current['sitemap_member'] is True:
            flags.append('sitemap_intent_conflict_review')
        if r['intent']=='unknown' or expected is None:
            deferred.append('preferred_identity_or_intent_unknown')
        if state!='complete':
            deferred.append('current_capture_incomplete')
        if status is None:
            deferred.append('response_status_unknown')
        if any(current[k] is None for k in ('http_noindex','initial_noindex','rendered_noindex')):
            deferred.append('directive_observations_incomplete')
        if current['robots']=='disallowed' and any(current[k] is True for k in ('http_noindex','initial_noindex','rendered_noindex')):
            flags.append('disallow_may_prevent_directive_discovery_review')
        known = [v for k in fields if current[k] is not None for v in current[k]]
        if len(set(known))>1:
            flags.append('different_canonical_targets_review')
        if any(current[k] is not None and len(current[k])>1 for k in fields):
            flags.append('multiple_canonical_declarations_review')
        if expected is not None and any(v!=expected for v in known):
            flags.append('declared_canonical_differs_from_preference_review')
        if any(current[k] is None for k in fields):
            deferred.append('canonical_groups_incomplete')
        if state=='complete' and status==200 and all(current[k] is not None for k in fields):
            if len(set(known))==1 and known[0]!=u:
                edges[u]=known[0]
        comparison = 'not_assessed'
        if inspected is None:
            deferred.append('processed_search_evidence_unavailable')
        elif changed is None or inspected['last_crawl_at'] is None:
            deferred.append('processed_recency_not_established')
        elif time(inspected['last_crawl_at'])<time(changed):
            comparison='predates_declared_change'
            deferred.append('processed_sample_predates_change')
        else:
            comparison='crawl_at_or_after_declared_change'
            if inspected['selected_canonical'] is None:
                deferred.append('selected_canonical_unavailable')
            elif expected is not None and inspected['selected_canonical']!=expected:
                flags.append('processed_selected_canonical_differs_review')
            if r['intent']=='representative' and inspected['state']=='not_indexed':
                flags.append('processed_representative_not_indexed_review')
            if r['intent'] in ('excluded','protected') and inspected['state']=='indexed':
                flags.append('processed_exclusion_intent_review')
            if inspected['state']=='unknown':
                deferred.append('processed_state_unknown')
        results.append({'id':ident,'url':u,'current_ref':current['evidence_ref'],
                        'processed_ref':None if inspected is None else inspected['evidence_ref'],
                        'processed_recency':comparison,'review_findings':flags,'deferred_checks':deferred})
    out = {r['url']:r for r in results}
    for u,target in edges.items():
        result=out[u]
        if target not in by_url:
            result['deferred_checks'].append('canonical_target_not_in_supplied_inventory')
        else:
            t=by_url[target]['current']
            if t['status']=='complete' and t['http_status'] is not None and t['http_status']!=200:
                result['review_findings'].append('canonical_target_non_200_review')
            elif t['status']!='complete' or t['http_status'] is None:
                result['deferred_checks'].append('canonical_target_response_unverified')
            if any(t[k] is True for k in ('http_noindex','initial_noindex','rendered_noindex')):
                result['review_findings'].append('canonical_target_noindex_review')
            if t['robots']=='disallowed':
                result['review_findings'].append('canonical_target_disallowed_review')
            if target in edges:
                result['review_findings'].append('canonical_chain_or_cycle_review')
    done=set()
    for start in edges:
        path, position = [], {}
        node=start
        while node in edges and node not in done and node not in position:
            position[node]=len(path)
            path.append(node)
            node=edges[node]
        if node in position:
            for member in path[position[node]:]:
                out[member]['review_findings'].append('canonical_cycle_review')
        done.update(path)
    return {'method':METHOD,'scope':data['scope'],'urls':results,'review_required':True,
            'limits':'Reviewed local projection only. No live fetch, directive parsing, URL normalization, search API, content equivalence, index guarantee or causal proof. Recency is last crawl vs supplied change, not proof of processing that revision.'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    try:
        data=json.loads(args.input.read_text(encoding='utf-8'),object_pairs_hook=unique_object)
        report=audit(data)
        with args.output.open('x',encoding='utf-8') as out:
            json.dump(report,out,ensure_ascii=False,indent=2,allow_nan=False)
            out.write('\n')
    except (OSError,ValueError,KeyError,TypeError,AttributeError) as exc:
        print('Index evidence review failed:',exc)
        return 1
    print('Supplied indexing evidence processed; review required.')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
