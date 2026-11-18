#!/usr/bin/env python3
"""Review supplied field percentiles and matched lab runs independently."""
import argparse
import json
import math
from datetime import date
from decimal import Decimal
from pathlib import Path
from statistics import median

METHOD = 'T09-v1'
CWV = {'lcp_ms': (2500, 4000), 'inp_ms': (200, 500), 'cls': (0.1, 0.25)}
LAB = {'lcp_ms', 'cls', 'tbt_ms', 'ttfb_ms', 'interaction_ms', 'transfer_bytes'}


def text(v):
    return isinstance(v, str) and bool(v.strip())


def number(v):
    return type(v) in (int, float) and math.isfinite(v) and v >= 0


def unique_object(pairs):
    obj = {}
    for k, v in pairs:
        if k in obj:
            raise ValueError('duplicate JSON key')
        obj[k] = v
    return obj


def day(v):
    d = date.fromisoformat(v)
    if d.isoformat() != v:
        raise ValueError('expected YYYY-MM-DD')
    return d


def classification(metric, value):
    good, poor = CWV[metric]
    return 'good' if value <= good else 'poor' if value > poor else 'needs_improvement'


def field_report(f):
    if not text(f['id']) or not text(f['subject']) or not text(f['evidence_ref']) or not text(f['method']):
        raise ValueError('field identity/provenance required')
    if f['source'] not in ('crux', 'rum', 'other') or f['level'] not in ('url', 'origin', 'route_group'):
        raise ValueError('invalid field source/level')
    if f['device'] not in ('mobile','desktop','tablet','all','unknown'):
        raise ValueError('invalid device')
    if day(f['start']) > day(f['end']):
        raise ValueError('invalid field window')
    metrics = f['p75']
    if not isinstance(metrics,dict) or set(metrics)!=set(CWV):
        raise ValueError('expected exact CWV p75 groups')
    out = {}
    for k,v in metrics.items():
        if v is not None and not number(v):
            raise ValueError('field values must be nonnegative finite numbers or null')
        out[k] = {'value': v, 'classification': None if v is None else classification(k,v)}
    # Conservative local summary: never substitute origin data for a URL,
    # or pretend PSI's special missing-INP assessment is our assessment.
    statuses = [x['classification'] for x in out.values()]
    summary = ('incomplete' if None in statuses else
               'all_three_good' if all(x=='good' for x in statuses) else 'not_all_good')
    return {k:f[k] for k in ('id','source','level','subject','device','start','end','method','evidence_ref')} | {
        'p75':out,'local_summary':summary}


def lab_report(c):
    if not text(c['id']) or not text(c['expected_profile']) or not text(c['baseline_revision']) or not text(c['candidate_revision']) or c['baseline_revision']==c['candidate_revision']:
        raise ValueError('distinct reviewed revisions and profile required')
    metric=c['metric']
    if metric not in LAB or not number(c['allowed_regression']):
        raise ValueError('invalid lab metric or absolute tolerance')
    minimum=c['minimum_runs']
    if type(minimum) is not int or not 3<=minimum<=30:
        raise ValueError('minimum runs must be 3–30')
    results={}
    seen=set()
    reasons=[]
    for arm,rev in (('baseline',c['baseline_revision']),('candidate',c['candidate_revision'])):
        runs=c[arm]
        if not isinstance(runs,list) or len(runs)>30:
            raise ValueError('expected at most 30 planned runs per arm')
        values=[]
        for r in runs:
            if not text(r['id']) or r['id'] in seen or not text(r['profile']) or not text(r['revision']):
                raise ValueError('unique run ID and profile/revision required')
            seen.add(r['id'])
            state=r['status']
            if state not in ('complete','partial','failed','not_collected'):
                raise ValueError('invalid lab run state')
            if state=='not_collected':
                if r['evidence_ref'] is not None:
                    raise ValueError('uncollected run cannot claim evidence')
            elif not text(r['evidence_ref']):
                raise ValueError('attempted run requires evidence reference')
            value=r['value']
            if state=='complete':
                if not number(value):
                    raise ValueError('complete run needs finite nonnegative measurement')
            elif value is not None:
                raise ValueError('incomplete run must not assert comparable value')
            if state!='complete' or r['profile']!=c['expected_profile'] or r['revision']!=rev:
                reasons.append(arm+':incomplete_or_mismatched_run')
            else:
                values.append(Decimal(str(value)))
        if len(values)<minimum:
            reasons.append(arm+':insufficient_comparable_runs')
        results[arm]={'planned':len(runs),'comparable':len(values),
                      'median':float(median(values)) if values else None,
                      'range':[float(min(values)),float(max(values))] if values else None}
    # Do not silently drop failed/mismatched runs or compare unequal planned cohorts.
    if len(c['baseline'])!=len(c['candidate']):
        reasons.append('unequal_planned_run_counts')
    delta=None
    status='deferred'
    if not reasons:
        d=Decimal(str(results['candidate']['median']))-Decimal(str(results['baseline']['median']))
        delta=float(d)
        status='regression_review' if d>Decimal(str(c['allowed_regression'])) else 'within_reviewed_tolerance'
    return {'id':c['id'],'metric':metric,'baseline_revision':c['baseline_revision'],
            'candidate_revision':c['candidate_revision'],'profile':c['expected_profile'],
            **results,'delta':delta,'allowed_regression':c['allowed_regression'],
            'status':status,'deferred_checks':sorted(set(reasons)),
            'evidence_refs':{arm:[r['evidence_ref'] for r in c[arm]] for arm in ('baseline','candidate')}}


def audit(data):
    json.dumps(data,allow_nan=False)
    if data['schema_version']!='1' or not text(data['scope']):
        raise ValueError('invalid local QA envelope')
    fields, labs=data['field'],data['lab']
    if not isinstance(fields,list) or not isinstance(labs,list) or len(fields)>500 or len(labs)>500 or not (fields or labs):
        raise ValueError('expected 1–1000 reviewed records, at most 500 per kind')
    for rows in (fields,labs):
        ids=[r['id'] for r in rows]
        if not all(text(x) for x in ids) or len(set(ids))!=len(ids):
            raise ValueError('unique record IDs required per kind')
    return {'method':METHOD,'scope':data['scope'],'field':[field_report(f) for f in fields],
            'lab':[lab_report(c) for c in labs],'review_required':True,
            'limits':'Supplied field p75 and controlled lab values only; no collection, rollup, field window comparison, PSI assessment reproduction, causal or statistical significance claim, UX acceptance or ranking prediction. Lab thresholds are project tolerances, not field CWV thresholds.'}


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
    except (OSError,ValueError,TypeError,KeyError,AttributeError,OverflowError) as exc:
        print('Performance evidence review failed:',exc)
        return 1
    print('Supplied performance evidence processed; review required.')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
