#!/usr/bin/env python3
"""Prepare prompt-only tasks and aggregate independently reviewed paired runs."""
import argparse
import hashlib
import json
from pathlib import Path

ARMS = ('baseline', 'skill')
EXPECTED = ('pass', 'fail', 'not_observable')
DISQUALIFIERS = ('absent', 'observed', 'not_observable')


def nonempty(x):
    return isinstance(x, str) and bool(x.strip())


def fingerprint(data):
    return hashlib.sha256(json.dumps(data, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def cases_index(suite):
    if not nonempty(suite['version']) or not isinstance(suite['cases'], list) or not suite['cases']:
        raise ValueError('invalid suite')
    index = {}
    for case in suite['cases']:
        ident = case['id']
        if not nonempty(ident) or ident in index or not nonempty(case['prompt']):
            raise ValueError('invalid or duplicate case')
        for key in ('expected', 'disqualifiers'):
            values = case[key]
            if not isinstance(values, list) or not values or not all(map(nonempty, values)):
                raise ValueError('invalid criteria')
        index[ident] = case
    return index


def prepare(suite, config):
    cases = cases_index(suite)
    for key in ('model', 'runtime', 'tool_config', 'permission_mode', 'skill_commit',
                'launch_protocol', 'review_protocol'):
        if not nonempty(config[key]):
            raise ValueError('missing experiment configuration: ' + key)
    if config['suite_kind'] not in ('public_regression', 'held_out'):
        raise ValueError('invalid suite kind')
    repeats = config['repeats']
    if type(repeats) is not int or not 1 <= repeats <= 20:
        raise ValueError('repeats must be 1–20')
    return {'schema_version':'1', 'suite_sha256':fingerprint(suite), 'config':config,
            'tasks':[{'case_id':ident, 'repeat':n, 'prompt':case['prompt']}
                     for ident,case in cases.items() for n in range(1,repeats+1)]}


def grade_items(items, count, allowed):
    if not isinstance(items, list) or len(items) != count:
        raise ValueError('incomplete criterion grading')
    seen = {}
    for item in items:
        n = item['criterion']
        if type(n) is not int or not 1 <= n <= count or n in seen:
            raise ValueError('invalid or duplicate criterion index')
        if item['status'] not in allowed or not nonempty(item['evidence']):
            raise ValueError('criterion requires status and evidence/rationale')
        seen[n] = item['status']
    return list(seen.values())


def score(suite, plan, grades):
    if plan != prepare(suite, plan['config']):
        raise ValueError('plan does not match frozen suite/config')
    if grades['plan_sha256'] != fingerprint(plan):
        raise ValueError('grades do not match frozen plan')
    cases = cases_index(suite)
    slots = {(t['case_id'],t['repeat'],a) for t in plan['tasks'] for a in ARMS}
    rows = {}
    if not isinstance(grades['runs'], list):
        raise ValueError('runs must be an array')
    for row in grades['runs']:
        key = (row['case_id'],row['repeat'],row['arm'])
        if type(row['repeat']) is not int or key not in slots or key in rows:
            raise ValueError('unexpected or duplicate run')
        if not all(nonempty(row[k]) for k in ('output_ref','reviewer','trace_ref')):
            raise ValueError('missing output, trace or reviewer reference')
        case = cases[key[0]]
        expected = grade_items(row['expected'],len(case['expected']),EXPECTED)
        disq = grade_items(row['disqualifiers'],len(case['disqualifiers']),DISQUALIFIERS)
        passed = expected.count('pass')
        critical = 'observed' in disq
        unknown = 'not_observable' in expected or 'not_observable' in disq
        # Conservative initial gate: all criteria are essential until explicitly redesigned.
        success = passed * 5 >= len(expected) * 4 and not critical and not unknown
        rows[key] = {'passed_criteria':passed,'total_criteria':len(expected),
                     'critical_failure':critical,'unobservable':unknown,'case_pass':success}
    pairs = [(rows[(i,n,'baseline')],rows[(i,n,'skill')])
             for i,n,a in sorted(slots) if a == 'baseline' and
             (i,n,'baseline') in rows and (i,n,'skill') in rows]
    summary = {}
    for pos, arm in enumerate(ARMS):
        graded = [r for k,r in rows.items() if k[2] == arm]
        matched = [p[pos] for p in pairs]
        p = sum(r['passed_criteria'] for r in matched)
        total = sum(r['total_criteria'] for r in matched)
        summary[arm] = {'graded_runs':len(graded),'matched_criteria_passed':p,
                        'matched_criteria_total':total,'matched_rate':p/total if total else None,
                        'matched_case_passes':sum(r['case_pass'] for r in matched),
                        'critical_failures_all_graded':sum(r['critical_failure'] for r in graded),
                        'unobservable_runs_all_graded':sum(r['unobservable'] for r in graded)}
    b,s = (summary[a]['matched_rate'] for a in ARMS)
    complete = len(rows) == len(slots)
    return {'schema_version':'1','suite_kind':plan['config']['suite_kind'],
            'planned_runs':len(slots),'graded_runs':len(rows),'matched_pairs':len(pairs),
            'complete':complete,'arms':summary,'matched_delta_percentage_points':
            (s-b)*100 if b is not None else None,
            'paired_case_outcomes':{'skill_only_pass':sum(not x['case_pass'] and y['case_pass'] for x,y in pairs),
                                    'baseline_only_pass':sum(x['case_pass'] and not y['case_pass'] for x,y in pairs),
                                    'both_pass':sum(x['case_pass'] and y['case_pass'] for x,y in pairs),
                                    'neither_pass':sum(not x['case_pass'] and not y['case_pass'] for x,y in pairs)},
            'missing_runs':[{'case_id':i,'repeat':n,'arm':a} for i,n,a in sorted(slots-rows.keys())],
            'skill_internal_case_gate':complete and all(r['case_pass'] for k,r in rows.items() if k[2]=='skill'),
            'review_required':True,'release_certified':False,
            'limitations':'Manual grades are attestations. No verification of actual execution, blinding, source truth or generalization.'}


def load(path):
    def object_hook(pairs):
        result = {}
        for k,v in pairs:
            if k in result:
                raise ValueError('duplicate JSON key')
            result[k] = v
        return result
    data = json.loads(Path(path).read_text(encoding='utf-8'),object_pairs_hook=object_hook)
    fingerprint(data)
    return data


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode', choices=('prepare','score'))
    p.add_argument('--suite',required=True)
    p.add_argument('--config')
    p.add_argument('--plan')
    p.add_argument('--grades')
    p.add_argument('--out',required=True,type=Path)
    a = p.parse_args()
    try:
        suite = load(a.suite)
        if a.mode == 'prepare':
            result = prepare(suite,load(a.config))
            result_hash = fingerprint(result)
        else:
            result = score(suite,load(a.plan),load(a.grades))
            result_hash = None
        with a.out.open('x',encoding='utf-8') as f:
            json.dump(result,f,ensure_ascii=False,indent=2,allow_nan=False)
            f.write('\n')
        if result_hash:
            print('Plan SHA-256 (canonical JSON):',result_hash)
        print('Written; independent execution and review required.')
    except (OSError,ValueError,TypeError,KeyError,AttributeError) as exc:
        print('Benchmark processing failed:',exc)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
