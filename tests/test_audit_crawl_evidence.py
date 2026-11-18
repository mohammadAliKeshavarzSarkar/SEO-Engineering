import unittest
from scripts.audit_crawl_evidence import audit


def row(**kw):
    r = dict(id='guide',purpose='acquisition',index_intent=True,sitemap_member=True,
             canonical_self=True,noindex=False,critical_resource=False,
             inbound_link_observed=True,collection='observed',http_status=200,
             robots='allowed',robots_ref='rules-1',robots_agent='Googlebot',
             evidence_ref='response-1',discovery=['sitemap','link'])
    r.update(kw)
    return r


def envelope(*rows, coverage='complete_declared_scope'):
    return dict(schema_version='1',scope='synthetic',crawler_policy='reviewed-example',
                coverage=coverage,stop_reason='bounded sample',urls=list(rows))


class CrawlEvidenceTests(unittest.TestCase):
    def result(self, **kw):
        return audit(envelope(row(**kw)))['urls'][0]

    def test_observed_not_index_proof(self):
        result = audit(envelope(row()))
        self.assertTrue(result['review_required'])
        self.assertEqual(result['urls'][0]['review_findings'],[])

    def test_disallowed_index_intent(self):
        r=self.result(robots='disallowed')
        self.assertIn('intended_index_route_disallowed_review',r['review_findings'])
        self.assertIn('sitemap_url_disallowed_review',r['review_findings'])

    def test_disallow_and_noindex(self):
        self.assertIn('disallow_may_prevent_noindex_discovery_review',
                      self.result(robots='disallowed',noindex=True)['review_findings'])

    def test_required_resource(self):
        self.assertIn('required_render_resource_disallowed_review',
                      self.result(robots='disallowed',critical_resource=True)['review_findings'])

    def test_sitemap_intent_and_response(self):
        r=self.result(purpose='redirect',http_status=301,canonical_self=None,noindex=None,index_intent=False)
        self.assertIn('sitemap_intent_conflict_review',r['review_findings'])
        self.assertIn('sitemap_response_status_review',r['review_findings'])

    def test_sitemap_canonical_and_noindex(self):
        r=self.result(canonical_self=False,noindex=True)
        self.assertIn('sitemap_canonical_preference_review',r['review_findings'])
        self.assertIn('sitemap_noindex_review',r['review_findings'])

    def test_partial_scope_not_orphan(self):
        r=audit(envelope(row(inbound_link_observed=False),coverage='partial'))['urls'][0]
        self.assertIn('no_inbound_link_claim_deferred_incomplete_scope',r['deferred_checks'])
        self.assertNotIn('no_inbound_link_in_declared_scope_review',r['review_findings'])

    def test_scoped_no_inbound(self):
        self.assertIn('no_inbound_link_in_declared_scope_review',
                      self.result(inbound_link_observed=False)['review_findings'])

    def test_unobserved_and_unknown(self):
        r=self.result(collection='not_attempted',http_status=None,canonical_self=None,noindex=None,
                      robots='unknown',robots_agent=None,robots_ref=None)
        self.assertIn('sitemap_response_unverified',r['deferred_checks'])
        self.assertIn('robots_decision_unavailable',r['deferred_checks'])
        self.assertEqual(r['review_findings'],[])

    def test_rate_and_availability(self):
        for status in (429,503):
            self.assertIn('rate_limit_or_server_availability_review',
                          self.result(http_status=status)['review_findings'])

    def test_invalid_inputs(self):
        for kw in (dict(http_status=True),dict(collection='failed'),dict(robots_ref=None),
                   dict(index_intent=1),dict(discovery=['sitemap','sitemap'])):
            with self.assertRaises(ValueError): self.result(**kw)

    def test_duplicate_and_nonfinite(self):
        with self.assertRaises(ValueError): audit(envelope(row(),row()))
        d=envelope(row());d['extra']=float('nan')
        with self.assertRaises(ValueError): audit(d)
