#!/usr/bin/env python3
"""Coordinate trusted offline SEO utilities and reviewed grouping; no crawler or shell."""
import argparse
import hashlib
import json
from pathlib import Path
if __package__:
    from . import inspect_architecture, audit_rendering, audit_spa_build, audit_next_delivery
    from . import audit_crawl_evidence, audit_index_evidence, audit_migration, audit_metadata
    from . import audit_performance, prioritize_opportunities
else:
    import inspect_architecture, audit_rendering, audit_spa_build, audit_next_delivery
    import audit_crawl_evidence, audit_index_evidence, audit_migration, audit_metadata
    import audit_performance, prioritize_opportunities

METHOD = 'T10-v1'
MODULES = {
    'T01': (inspect_architecture, inspect_architecture.summarize),
    'T02': (audit_rendering, audit_rendering.audit),
    'T03': (audit_spa_build, audit_spa_build.audit),
    'T04': (audit_next_delivery, audit_next_delivery.audit),
    'T05': (audit_crawl_evidence, audit_crawl_evidence.audit),
    'T06': (audit_index_evidence, audit_index_evidence.audit),
    'T07': (audit_migration, audit_migration.audit),
    'T08': (audit_metadata, audit_metadata.audit),
    'T09': (audit_performance, audit_performance.audit),
}
T01_DEFERRED = {'authorization_unverified', 'missing_route_status_unknown',
                'redirect_status_unknown', 'redirect_destination_not_checked',
                'public_status_unknown', 'initial_index_directive_unknown',
                'rendered_content_unknown', 'collect_source_and_render_evidence'}
ESCALATE = {'suspected_private_content_exposure_escalate',
            'suspected_unauthorized_payload_exposure_escalate'}


def text(v):
    return isinstance(v, str) and bool(v.strip())


def unique_object(pairs):
    result = {}
    for k, v in pairs:
        if k in result:
            raise ValueError('duplicate JSON key')
        result[k] = v
    return result


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     allow_nan=False, separators=(',', ':')).encode('utf-8')).hexdigest()


def get_signals(module_id, report, report_hash, binding_hash):
    """Explicit adapters for pinned native output layouts, not a generic JSON scan."""
    signals = []

    def add(pointer, record_id, kind, detail):
        code = detail if isinstance(detail, str) else detail['code']
        if not text(code):
            raise ValueError('invalid native signal')
        signals.append({'id':module_id + ':' + binding_hash + ':' + pointer,
                        'module':module_id, 'record_id':record_id, 'pointer':pointer,
                        'report_sha256':report_hash, 'binding_sha256':binding_hash, 'kind':kind, 'code':code,
                        'detail':detail, 'escalation_review':code in ESCALATE})

    def lists(obj, base, record_id, names=('review_findings','deferred_checks')):
        for field in names:
            for j, detail in enumerate(obj[field]):
                add(base+'/'+field+'/'+str(j), record_id,
                    'deferred' if field=='deferred_checks' else 'review_candidate', detail)

    if module_id == 'T01':
        for i, row in enumerate(report['routes']):
            for j, code in enumerate(row['findings']):
                add(f'/routes/{i}/findings/{j}',row['id'],
                    'deferred' if code in T01_DEFERRED else 'review_candidate',code)
    elif module_id in ('T02','T03','T04','T07'):
        for i, row in enumerate(report['routes']):
            base=f'/routes/{i}'
            lists(row,base,row['id'])
            if module_id=='T04':
                for j,sample in enumerate(row['samples']):
                    lists(sample,base+f'/samples/{j}',row['id'])
    elif module_id in ('T05','T06'):
        for i,row in enumerate(report['urls']):
            lists(row,f'/urls/{i}',row['id'])
    elif module_id=='T08':
        for i,row in enumerate(report['pages']):
            base=f'/pages/{i}'
            lists(row,base,row['id'],('plan_review_findings',))
            for capture in ('source','rendered'):
                lists(row['captures'][capture],base+'/captures/'+capture,row['id'])
    elif module_id=='T09':
        for i,row in enumerate(report['field']):
            for metric,value in row['p75'].items():
                state=value['classification']
                if state!='good':
                    add(f'/field/{i}/p75/{metric}',row['id'],
                        'deferred' if state is None else 'review_candidate',
                        {'code':'field_metric_unknown' if state is None else 'field_metric_review',
                         'metric':metric,'classification':state})
        for i,row in enumerate(report['lab']):
            lists(row,f'/lab/{i}',row['id'],('deferred_checks',))
            if row['status']=='regression_review':
                add(f'/lab/{i}/status',row['id'],'review_candidate','lab_regression_review')
    else:
        raise ValueError('unsupported native report')
    return signals


def group_signals(groups, signals):
    if not isinstance(groups,list) or len(groups)>5000:
        raise ValueError('expected bounded reviewed groups')
    candidates={s['id']:s for s in signals if s['kind']=='review_candidate'}
    used,ids=set(),set()
    backlog=[]
    for g in groups:
        ident=g['id']
        if not text(ident) or ident in ids or not all(text(g[k]) for k in
                ('reviewer','scope','rationale','owner','next_check')):
            raise ValueError('unique group ID and reviewed context required')
        ids.add(ident)
        refs=g['signal_ids']
        if (not isinstance(refs,list) or not refs or not all(text(x) and x in candidates for x in refs)
                or len(set(refs))!=len(refs) or used.intersection(refs)):
            raise ValueError('group needs unique unassigned current candidate references')
        used.update(refs)
        # R08 receives reviewed values only. T10 does not mark any issue verified.
        backlog.append({k:g[k] for k in ('id','severity','fit','risk','confidence',
                                         'impact','effort_days','depends_on')} | {'status':'pending'})
    return {'groups':groups,'ungrouped_candidate_ids':sorted(candidates.keys()-used),
            'triage':prioritize_opportunities.prioritize(backlog) if backlog else None}


def audit(data, artifact_root=None):
    json.dumps(data,allow_nan=False)
    if data['schema_version']!='1' or not all(text(data[k]) for k in
            ('scope','audit_id','context_ref','reviewed_revision')):
        raise ValueError('invalid audit envelope')
    tasks=data['tasks']
    if not isinstance(tasks,dict) or set(tasks)!=set(MODULES):
        raise ValueError('explicit task state required for each T01–T09')
    for key,task in tasks.items():
        if task['state'] not in ('ready','blocked','not_applicable') or not text(task['reason']):
            raise ValueError('invalid task state or missing reason')
        if task['state']=='ready':
            if not isinstance(task['input'],dict) or not text(task['input_ref']):
                raise ValueError('ready task needs local input and reference')
        elif task['input'] is not None or task['input_ref'] is not None:
            raise ValueError('unrun task cannot assert input')
    rows,signals=[],[]
    for key,(module,run) in MODULES.items():
        task=tasks[key]
        row={'module':key,'planned_state':task['state'],'reason':task['reason'],
             'input_ref':task['input_ref'],'input_sha256':None,'report_sha256':None,
             'native_report':None,'status':task['state'],'failure_type':None,
             'utility_sha256':hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()}
        if task['state']=='ready':
            payload=task['input']
            row['input_sha256']=digest(payload)
            if key=='T03' and artifact_root is None:
                row['status']='blocked'
                row['reason']='explicit trusted artifact root not supplied'
            else:
                try:
                    report=run(payload,artifact_root) if key=='T03' else run(payload)
                    if key=='T01':
                        if report['schema_version']!='1':
                            raise ValueError('unexpected native report version')
                    elif report['method']!=key+'-v1':
                        raise ValueError('unexpected native report version')
                    h=digest(report)
                    binding=digest({'audit_id':data['audit_id'],'scope':data['scope'],
                                    'context_ref':data['context_ref'],'revision':data['reviewed_revision'],
                                    'module':key,'input_ref':task['input_ref'],
                                    'input_sha256':row['input_sha256'],'report_sha256':h,
                                    'utility_sha256':row['utility_sha256']})
                    found=get_signals(key,report,h,binding)
                    row.update(status='processed',native_report=report,report_sha256=h)
                    signals.extend(found)
                except (ValueError,TypeError,KeyError,AttributeError,OSError,OverflowError,RecursionError) as exc:
                    # Avoid leaking arbitrary contents from malformed input into logs.
                    row.update(status='failed',failure_type=type(exc).__name__)
        rows.append(row)
    grouped=group_signals(data['groups'],signals)
    counts={s:sum(r['status']==s for r in rows) for s in ('processed','blocked','not_applicable','failed')}
    return {'method':METHOD,'audit_id':data['audit_id'],'scope':data['scope'],
            'context_ref':data['context_ref'],'reviewed_revision':data['reviewed_revision'],
            'manifest_sha256':digest(data),'modules':rows,'signals':signals,
            'coverage':{'module_counts':counts,'review_candidates':sum(s['kind']=='review_candidate' for s in signals),
                        'deferred_signals':sum(s['kind']=='deferred' for s in signals),
                        'escalation_candidate_ids':[s['id'] for s in signals if s['escalation_review']]},
            **grouped,'review_required':True,'authorization_required':True,
            'limits':'Offline coordination of supplied local projections only. Processed is not pass; counts are modules/signals, not unique issues, coverage of site, health score or search outcome. Scope, comparability, authorization, grouping and severity are reviewed inputs, not independently verified. Hashes identify local input/report/code, not authenticity or complete artifact contents. No network, deployment or automatic fixes.'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    p.add_argument('--artifact-root',type=Path,help='Explicit trusted local root for T03 only')
    args=p.parse_args()
    try:
        with args.input.open('rb') as stream:
            raw=stream.read(16*1024*1024+1)
        if len(raw)>16*1024*1024:
            raise ValueError('manifest exceeds 16 MiB')
        data=json.loads(raw.decode('utf-8'),object_pairs_hook=unique_object)
        report=audit(data,args.artifact_root)
        with args.output.open('x',encoding='utf-8') as out:
            json.dump(report,out,indent=2,ensure_ascii=False,allow_nan=False)
            out.write('\n')
    except (OSError,ValueError,TypeError,KeyError,AttributeError,OverflowError,RecursionError) as exc:
        print('Audit coordination failed:',type(exc).__name__)
        return 1
    print('Offline audit report written; review required.')
    return 2 if report['coverage']['module_counts']['failed'] else 0


if __name__=='__main__':
    raise SystemExit(main())
