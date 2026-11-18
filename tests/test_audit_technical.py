import json
import unittest
from pathlib import Path
from scripts.audit_technical import audit, MODULES, digest

ROOT=Path(__file__).resolve().parent.parent

def fixture():
    return json.loads((ROOT/'examples/technical-audit/sample.json').read_text(encoding='utf-8'))

def group(ref,**kw):
    g=dict(id='review-1',scope='reviewed synthetic issue',reviewer='fixture reviewer',
           rationale='reviewed relationship',owner='fixture owner',next_check='verify',
           signal_ids=[ref],severity='P1',fit='eligible',risk='low',confidence='high',
           impact=None,effort_days=None,depends_on=[])
    g.update(kw)
    return g

class TechnicalAuditTests(unittest.TestCase):
    def run_audit(self,d=None):
        return audit(fixture() if d is None else d,ROOT/'examples/spa-build/artifacts')

    def test_all_nine_real_utilities(self):
        r=self.run_audit()
        self.assertEqual(r['coverage']['module_counts']['processed'],9)
        self.assertEqual({x['module'] for x in r['modules']},set(MODULES))
        self.assertTrue(r['review_required'])
        self.assertTrue(r['authorization_required'])
        self.assertGreater(r['coverage']['review_candidates'],0)
        self.assertGreater(r['coverage']['deferred_signals'],0)

    def test_deterministic_and_hashes(self):
        a,b=self.run_audit(),self.run_audit()
        self.assertEqual(a,b)
        for r in a['modules']:
            self.assertEqual(r['report_sha256'],digest(r['native_report']))
        self.assertEqual(len({s['id'] for s in a['signals']}),len(a['signals']))

    def test_native_pointer_integrity(self):
        r=self.run_audit()
        reports={x['module']:x['native_report'] for x in r['modules']}
        for s in r['signals']:
            obj=reports[s['module']]
            for key in s['pointer'].split('/')[1:]:
                obj=obj[int(key)] if isinstance(obj,list) else obj[key]
            if s['module']!='T09':
                self.assertEqual(obj,s['detail'])

    def test_explicit_blocked_and_na(self):
        d=fixture()
        for m,state in (('T02','blocked'),('T04','not_applicable')):
            d['tasks'][m]=dict(state=state,reason='fixture reason',input=None,input_ref=None)
        r=self.run_audit(d)
        self.assertEqual(r['coverage']['module_counts'],dict(processed=7,blocked=1,not_applicable=1,failed=0))

    def test_missing_artifact_root_blocks_only_t03(self):
        r=audit(fixture())
        self.assertEqual(r['coverage']['module_counts']['blocked'],1)
        self.assertEqual(r['modules'][2]['status'],'blocked')

    def test_malformed_task_is_failed_not_pass(self):
        d=fixture();d['tasks']['T02']['input']={}
        r=self.run_audit(d)
        self.assertEqual(r['modules'][1]['status'],'failed')
        self.assertIsNone(r['modules'][1]['native_report'])
        self.assertEqual(r['coverage']['module_counts']['processed'],8)

    def test_requires_explicit_states(self):
        d=fixture();del d['tasks']['T09']
        with self.assertRaises(ValueError): self.run_audit(d)
        d=fixture();d['tasks']['exec']=d['tasks']['T01']
        with self.assertRaises(ValueError): self.run_audit(d)

    def test_reviewed_group_and_r08(self):
        d=fixture();r=self.run_audit(d)
        ref=next(s['id'] for s in r['signals'] if s['kind']=='review_candidate')
        d['groups']=[group(ref)]
        out=self.run_audit(d)
        self.assertEqual(out['triage']['rows'][0]['lane'],'repair')
        self.assertNotIn(ref,out['ungrouped_candidate_ids'])

    def test_no_auto_dedup_and_deferred_not_groupable(self):
        d=fixture();r=self.run_audit(d)
        self.assertEqual(len(r['ungrouped_candidate_ids']),r['coverage']['review_candidates'])
        ref=next(s['id'] for s in r['signals'] if s['kind']=='deferred')
        d['groups']=[group(ref)]
        with self.assertRaises(ValueError): self.run_audit(d)

    def test_stale_duplicate_and_dependency_groups_rejected(self):
        d=fixture();r=self.run_audit(d)
        ref=next(s['id'] for s in r['signals'] if s['kind']=='review_candidate')
        for groups in ([group('stale')],[group(ref),group(ref,id='other')],
                       [group(ref,depends_on=['absent'])]):
            d['groups']=groups
            with self.assertRaises(ValueError): self.run_audit(d)

    def test_escalation_survives_grouping(self):
        d=fixture()
        row=d['tasks']['T01']['input']['routes'][0]
        row.update(expected='private',unauthorized_content_visible=True)
        r=self.run_audit(d)
        refs=r['coverage']['escalation_candidate_ids']
        self.assertTrue(refs)
        self.assertTrue(any(s['code']=='suspected_private_content_exposure_escalate'
                            for s in r['signals'] if s['id'] in refs))

    def test_changed_input_invalidates_prior_group_even_if_report_same(self):
        d=fixture(); r=self.run_audit(d)
        ref=next(s['id'] for s in r['signals'] if s['kind']=='review_candidate')
        signal=next(s for s in r['signals'] if s['id']==ref)
        d['tasks'][signal['module']]['input_ref']='fixture:changed-evidence-ref'
        d['groups']=[group(ref)]
        with self.assertRaises(ValueError): self.run_audit(d)

    def test_nonfinite_rejected(self):
        d=fixture();d['x']=float('nan')
        with self.assertRaises(ValueError): self.run_audit(d)
