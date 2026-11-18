import unittest
from scripts.audit_performance import audit,classification

def field(**kw):
    r=dict(id='f',source='crux',level='url',subject='https://example.org/guide/',device='mobile',
           start='2026-10-21',end='2026-11-17',method='fixture:p75',evidence_ref='fixture:field',
           p75=dict(lcp_ms=2500,inp_ms=200,cls=0.1))
    r.update(kw)
    return r

def runs(arm,values):
    return [dict(id=arm+str(i),revision=arm,profile='fixed',status='complete',value=v,evidence_ref='fixture:'+arm+str(i))
            for i,v in enumerate(values)]

def lab(**kw):
    r=dict(id='l',metric='lcp_ms',expected_profile='fixed',baseline_revision='old',candidate_revision='new',
           minimum_runs=3,allowed_regression=100,baseline=runs('old',[2000,2100,2200]),candidate=runs('new',[2100,2200,2300]))
    r.update(kw)
    return r

def envelope(f=None,l=None):
    return dict(schema_version='1',scope='synthetic',field=f or [],lab=l or [])

class PerformanceTests(unittest.TestCase):
    def test_threshold_boundaries(self):
        for k,g,p in [('lcp_ms',2500,4000),('inp_ms',200,500),('cls',0.1,0.25)]:
            self.assertEqual(classification(k,g),'good')
            self.assertEqual(classification(k,p),'needs_improvement')
            self.assertEqual(classification(k,p+0.01),'poor')
    def test_field_all_good(self):
        r=audit(envelope([field()]))
        self.assertEqual(r['field'][0]['local_summary'],'all_three_good')
        self.assertTrue(r['review_required'])
    def test_missing_inp_remains_unknown(self):
        r=audit(envelope([field(p75=dict(lcp_ms=2000,inp_ms=None,cls=0.05))]))['field'][0]
        self.assertEqual(r['local_summary'],'incomplete')
    def test_origin_not_url(self):
        r=audit(envelope([field(level='origin',subject='https://example.org')]))['field'][0]
        self.assertEqual(r['level'],'origin')
    def test_lab_tolerance_boundary(self):
        r=audit(envelope(l=[lab()]))['lab'][0]
        self.assertEqual(r['delta'],100)
        self.assertEqual(r['status'],'within_reviewed_tolerance')
    def test_regression(self):
        r=audit(envelope(l=[lab(candidate=runs('new',[2400,2500,2600]))]))['lab'][0]
        self.assertEqual(r['status'],'regression_review')
    def test_cls_decimal_boundary(self):
        r=audit(envelope(l=[lab(metric='cls',allowed_regression=0.1,baseline=runs('old',[0.2]*3),candidate=runs('new',[0.3]*3))]))['lab'][0]
        self.assertEqual(r['status'],'within_reviewed_tolerance')
    def test_mismatched_run(self):
        l=lab();l['candidate'][0]['profile']='other'
        r=audit(envelope(l=[l]))['lab'][0]
        self.assertEqual(r['status'],'deferred')
        self.assertIsNone(r['delta'])
    def test_failed_not_dropped(self):
        l=lab(candidate=runs('new',[1,2,3,4]),baseline=runs('old',[1,2,3,4]))
        l['candidate'][0].update(status='failed',value=None)
        r=audit(envelope(l=[l]))['lab'][0]
        self.assertEqual(r['candidate']['comparable'],3)
        self.assertEqual(r['status'],'deferred')
    def test_unequal_cohorts(self):
        r=audit(envelope(l=[lab(candidate=runs('new',[1,2,3,4]))]))['lab'][0]
        self.assertIn('unequal_planned_run_counts',r['deferred_checks'])
    def test_tbt_not_inp(self):
        r=audit(envelope(l=[lab(metric='tbt_ms')]))
        self.assertEqual(r['field'],[])
        self.assertEqual(r['lab'][0]['metric'],'tbt_ms')
    def test_invalid_values(self):
        for v in (True,-1,float('nan'),float('inf')):
            with self.assertRaises(ValueError): audit(envelope([field(p75=dict(lcp_ms=v,inp_ms=1,cls=0))]))
    def test_invalid_window_and_duplicate(self):
        with self.assertRaises(ValueError): audit(envelope([field(start='2026-11-18')]))
        with self.assertRaises(ValueError): audit(envelope([field(),field()]))
    def test_incomplete_cannot_assert_measurement(self):
        l=lab();l['baseline'][0]['status']='partial'
        with self.assertRaises(ValueError): audit(envelope(l=[l]))
