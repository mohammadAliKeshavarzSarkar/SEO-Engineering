import unittest
from scripts.audit_next_delivery import audit


def sample(**kw):
    s = dict(id='s1',context_id='release-public-en',capture_status='complete',
             evidence_ref='fixture-1',observed_at='2026-11-18T10:05:00Z',
             http_status=200,content_revision='v2',private_payload_visible=None)
    s.update(kw)
    return s


def route(**kw):
    r = dict(id='guide',plan_ref='plan',next_major=16,router='app',
             cache_model='app_cache_components',deployment='runtime',strategy='hybrid',
             purpose='public',expected_context='release-public-en',required_features=[],
             expected_statuses=[200],expected_content_revision='v2',
             fresh_by='2026-11-18T10:05:00Z',samples=[sample()])
    r.update(kw)
    return r


def envelope(*rows):
    return dict(schema_version='1',scope='synthetic',routes=list(rows))


class NextDeliveryTests(unittest.TestCase):
    def row(self, **kw):
        return audit(envelope(route(**kw)))['routes'][0]

    def test_matching_observation_not_cache_proof(self):
        result = self.row()
        self.assertEqual(result['samples'][0]['freshness'],'target_observed')
        self.assertTrue(audit(envelope(route()))['review_required'])

    def test_before_deadline(self):
        r = self.row(samples=[sample(content_revision='v1',observed_at='2026-11-18T10:04:59Z')])
        self.assertEqual(r['samples'][0]['freshness'],'different_before_deadline')
        self.assertEqual(r['samples'][0]['review_findings'],[])

    def test_at_deadline_and_after(self):
        r = self.row(samples=[sample(content_revision='v1'),sample(id='s2',content_revision='v1',observed_at='2026-11-18T10:06:00Z')])
        for s in r['samples']:
            self.assertEqual(s['freshness'],'different_at_or_after_deadline')
            self.assertIn('freshness_target_not_observed_by_deadline_review',s['review_findings'])

    def test_mismatch_or_partial_defers(self):
        for s in (sample(context_id='other',content_revision='v1'),sample(capture_status='partial',content_revision='v1')):
            result = self.row(samples=[s])['samples'][0]
            self.assertEqual(result['freshness'],'not_assessed')
            self.assertEqual(result['review_findings'],[])

    def test_static_export_feature_conflict(self):
        r=self.row(deployment='static_export',strategy='isr',required_features=['isr','server_actions'])
        self.assertIn('static_export_runtime_strategy_conflict_review',r['review_findings'])
        self.assertIn('static_export_runtime_features_review',r['review_findings'])

    def test_router_version_and_unknown(self):
        self.assertIn('router_cache_model_conflict_review',self.row(router='pages')['review_findings'])
        self.assertIn('cache_components_version_compatibility_review',self.row(next_major=15)['review_findings'])
        self.assertIn('installed_version_router_cache_model_review',self.row(next_major=None)['deferred_checks'])

    def test_status_separate_from_freshness(self):
        s=self.row(purpose='missing',expected_statuses=[404],samples=[sample(content_revision=None)])['samples'][0]
        self.assertIn('http_status_differs_from_expectation_review',s['review_findings'])
        self.assertEqual(s['freshness'],'not_assessed')

    def test_exposure_escalation_independent(self):
        s=self.row(samples=[sample(capture_status='partial',context_id='other',private_payload_visible=True)])['samples'][0]
        self.assertIn('suspected_unauthorized_payload_exposure_escalate',s['review_findings'])

    def test_uncollected_and_failed(self):
        for state in ('failed','not_collected'):
            s=sample(capture_status=state,http_status=None,content_revision=None,
                     evidence_ref=None if state=='not_collected' else 'error',
                     observed_at=None if state=='not_collected' else '2026-11-18T10:05:00Z')
            result=self.row(samples=[s])['samples'][0]
            self.assertEqual(result['freshness'],'not_assessed')
        with self.assertRaises(ValueError): self.row(samples=[sample(capture_status='failed')])

    def test_no_target_and_no_sample(self):
        r=self.row(expected_content_revision=None,fresh_by=None,samples=[])
        self.assertIn('no_reviewed_freshness_target',r['deferred_checks'])
        self.assertIn('no_response_samples',r['deferred_checks'])

    def test_invalid_timestamps_and_types(self):
        for kw in (dict(fresh_by='2026-02-31T00:00:00Z'),dict(fresh_by=None),
                   dict(next_major=True),dict(expected_statuses=[True]),dict(required_features=['bogus']),
                   dict(samples=[sample(http_status=True)])):
            with self.assertRaises(ValueError): self.row(**kw)

    def test_duplicates_and_nonfinite(self):
        with self.assertRaises(ValueError): audit(envelope(route(),route()))
        with self.assertRaises(ValueError): self.row(samples=[sample(),sample()])
        d=envelope(route());d['extra']=float('nan')
        with self.assertRaises(ValueError): audit(d)
