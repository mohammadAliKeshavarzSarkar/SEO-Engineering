#!/usr/bin/env python3
"""Review explicit migration mappings and supplied HTTP GET traces; no fetching."""
import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

METHOD = 'T07-v1'
REDIRECTS = {301,302,303,307,308}
PERMANENT = {301,308}
TEMPORARY = {302,303,307}


def text(v):
    return isinstance(v,str) and bool(v.strip())


def absolute(v):
    if not text(v) or any(c.isspace() or ord(c)<32 or ord(c)==127 for c in v) or any(c in v for c in ('#','\\')) or re.search(r'%(?![0-9a-fA-F]{2})',v):
        return False
    try:
        p=urlsplit(v)
        _=p.port
        return p.scheme in ('http','https') and bool(p.hostname) and p.username is None and p.password is None
    except ValueError:
        return False


def origin(v):
    p=urlsplit(v)
    return (p.scheme,p.hostname,p.port or (443 if p.scheme=='https' else 80))


def identity(pairs):
    result={}
    for k,v in pairs:
        if k in result:
            raise ValueError('duplicate JSON key')
        result[k]=v
    return result


def audit(data):
    json.dumps(data,allow_nan=False)
    if data['schema_version']!='1' or not text(data['scope']) or not text(data['policy_version']):
        raise ValueError('invalid local QA envelope')
    allowed=data['allowed_origins']
    if not isinstance(allowed,list) or not 1<=len(allowed)<=100:
        raise ValueError('expected approved origins')
    origins=set()
    for v in allowed:
        if not absolute(v) or urlsplit(v).path not in ('','/') or '?' in v:
            raise ValueError('expected explicit origin without path or query')
        o=origin(v)
        if o in origins:
            raise ValueError('duplicate origin')
        origins.add(o)
    rows=data['routes']
    if not isinstance(rows,list) or not 1<=len(rows)<=5000:
        raise ValueError('expected 1–5000 mappings')
    by_url,ids,edges,results={},set(),{},[]
    for r in rows:
        u,ident=r['old_url'],r['id']
        if not absolute(u) or origin(u) not in origins or u in by_url or not text(ident) or ident in ids or not text(r['plan_ref']):
            raise ValueError('unique scoped old URL, ID and plan reference required')
        by_url[u]=r
        ids.add(ident)
        action=r['action']
        if action not in ('retain','permanent_redirect','temporary_redirect','remove','unknown'):
            raise ValueError('invalid reviewed action')
        target=r['target_url']
        if action in ('permanent_redirect','temporary_redirect'):
            if not absolute(target) or origin(target) not in origins:
                raise ValueError('redirect requires explicit approved target URL')
            edges[u]=target
        elif target is not None:
            raise ValueError('non-redirect action must have null target')
        expected=r['terminal_statuses']
        if expected is not None and (not isinstance(expected,list) or not expected or any(type(s)is not int or not 200<=s<=599 or s in REDIRECTS for s in expected) or len(set(expected))!=len(expected)):
            raise ValueError('invalid terminal status expectation')
        if action=='remove' and expected is not None and not set(expected)<= {404,410}:
            raise ValueError('removed public document expects 404/410')
        equivalent=r['replacement_reviewed']
        if equivalent is not None and type(equivalent)is not bool:
            raise ValueError('replacement review must be bool or null')
        if action not in ('permanent_redirect','temporary_redirect') and equivalent is not None:
            raise ValueError('replacement review applies only to redirect')
        flags, deferred=[],[]
        if action=='unknown':
            deferred.append('mapping_action_unknown')
        if action=='permanent_redirect' and equivalent is not True:
            flags.append('permanent_replacement_not_confirmed_review')
        if expected is None:
            deferred.append('terminal_status_expectation_unknown')
        trace=r['trace']
        state=trace['status']
        if state not in ('complete','partial','failed','not_collected'):
            raise ValueError('invalid trace state')
        ref=trace['evidence_ref']
        if state=='not_collected':
            if ref is not None:
                raise ValueError('uncollected trace must not assert evidence')
        elif not text(ref):
            raise ValueError('attempted trace requires evidence reference')
        if type(trace['context_matched']) is not bool and trace['context_matched'] is not None:
            raise ValueError('context_matched must be bool or null')
        hops=trace['transactions']
        if not isinstance(hops,list) or len(hops)>30:
            raise ValueError('expected at most 30 transactions')
        if state in ('failed','not_collected') and hops:
            raise ValueError('use partial for captured transaction prefix')
        if state=='complete' and not hops:
            raise ValueError('complete trace requires terminal response')
        if state!='complete' and state!='partial' and trace['context_matched'] is True:
            raise ValueError('no trace cannot establish matched context')
        visited=set()
        loop=False
        outside=False
        for i,h in enumerate(hops):
            hu,hs,next_url=h['url'],h['status'],h['resolved_location']
            if not absolute(hu) or origin(hu) not in origins or type(hs)is not int or not 200<=hs<=599 or not text(h['evidence_ref']):
                raise ValueError('invalid transaction identity or status')
            if i==0 and hu!=u:
                raise ValueError('trace must start at exact old URL')
            if next_url is not None and not absolute(next_url):
                raise ValueError('location must be reviewed resolved URL or null')
            if hs not in REDIRECTS and next_url is not None:
                raise ValueError('resolved redirect destination on non-followable response')
            if i and (hops[i-1]['status'] not in REDIRECTS or hops[i-1]['resolved_location']!=hu):
                raise ValueError('discontinuous observed transaction chain')
            if hu in visited or (hs in REDIRECTS and next_url in visited) or next_url==hu:
                loop=True
            visited.add(hu)
            if next_url is not None and origin(next_url) not in origins:
                outside=True
        if state=='complete' and (hops[-1]['status'] in REDIRECTS or hops[-1]['status']==304 or loop):
            raise ValueError('complete trace requires usable non-loop terminal response; use partial otherwise')
        if outside:
            flags.append('observed_redirect_outside_approved_origins_review')
        if loop:
            flags.append('observed_redirect_cycle_review')
        if any(h['status'] in REDIRECTS and h['resolved_location'] is None for h in hops):
            deferred.append('redirect_destination_unavailable')
        if len([h for h in hops if h['status'] in REDIRECTS])>1:
            flags.append('observed_multiple_redirect_hops_review')
        if trace['context_matched'] is not True:
            deferred.append('trace_context_not_established')
        if state!='complete':
            deferred.append('terminal_response_unverified')
        if trace['context_matched'] is True and hops:
            first=hops[0]['status']
            if action=='permanent_redirect' and first not in PERMANENT:
                flags.append('permanent_redirect_status_mismatch_review')
            if action=='temporary_redirect' and first not in TEMPORARY:
                flags.append('temporary_redirect_status_mismatch_review')
            if action in ('retain','remove') and first in REDIRECTS:
                flags.append('unexpected_redirect_review')
            if state=='complete':
                final=hops[-1]
                if target is not None and final['url']!=target:
                    flags.append('terminal_url_differs_from_reviewed_mapping')
                if expected is not None and final['status'] not in expected:
                    flags.append('terminal_status_differs_from_expectation')
        results.append({'id':ident,'old_url':u,'action':action,'target_url':target,
                        'plan_ref':r['plan_ref'],'trace_ref':ref,'trace_status':state,
                        'transaction_count':len(hops),'review_findings':flags,'deferred_checks':deferred})
    out={r['old_url']:r for r in results}
    for u,t in edges.items():
        if t in edges:
            out[u]['review_findings'].append('planned_redirect_chain_or_cycle_review')
        if t in by_url and by_url[t]['action']=='remove':
            out[u]['review_findings'].append('planned_target_removal_review')
    done=set()
    for start in edges:
        path,pos=[],{}
        node=start
        while node in edges and node not in done and node not in pos:
            pos[node]=len(path)
            path.append(node)
            node=edges[node]
        if node in pos:
            for member in path[pos[node]:]:
                out[member]['review_findings'].append('planned_redirect_cycle_review')
        done.update(path)
    return {'method':METHOD,'scope':data['scope'],'policy_version':data['policy_version'],
            'routes':results,'review_required':True,
            'limits':'Literal URL comparisons and supplied GET transaction prefixes only; no DNS, fetch, URL equivalence, full HTTP parser, server config generation, content equivalence, indexing, authorization verification or deployment proof. Origins are reviewed labels, not a network safety guard.'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    args=p.parse_args()
    try:
        data=json.loads(args.input.read_text(encoding='utf-8'),object_pairs_hook=identity)
        report=audit(data)
        with args.output.open('x',encoding='utf-8') as out:
            json.dump(report,out,ensure_ascii=False,indent=2,allow_nan=False)
            out.write('\n')
    except (OSError,ValueError,KeyError,TypeError,AttributeError) as exc:
        print('Migration review failed:',exc)
        return 1
    print('Supplied migration mappings processed; review findings and deferred checks.')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
