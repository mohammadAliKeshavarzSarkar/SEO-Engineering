import unittest
from scripts.audit_index_evidence import audit

A='https://example.org/a/'
B='https://example.org/b/'


def row(ident='a',u=A,**kw):
    cur=dict(status='complete',evidence_ref='fixture-current',observed_at='2026-11-18T10:00:00Z',
             http_status=200,robots='allowed',http_noindex=False,initial_noindex=False,
             rendered_noindex=False,sitemap_member=True,source_canonicals=[u],
             header_canonicals=[],rendered_canonicals=[u])
    r=dict(id=ident,url=u,intent='representative',preferred_url=u,changed_at='2026-11-17T00:00:00Z',
           current=cur,processed=None)
    r.update(kw)
    return r


def processed(**kw):
    p=dict(evidence_ref='fixture-processed',property='sc-domain:example.org',retrieved_at='2026-11-18T10:10:00Z',
           last_crawl_at='2026-11-18T09:00:00Z',state='indexed',user_canonical=A,selected_canonical=A)
    p.update(kw)
    return p


def envelope(*rows):
    return dict(schema_version='1',scope='synthetic',urls=list(rows))


class IndexEvidenceTests(unittest.TestCase):
    def review(self,r):
        return audit(envelope(r))['urls'][0]

    def test_live_not_processed(self):
        r=self.review(row())
        self.assertIn('processed_search_evidence_unavailable',r['deferred_checks'])
        self.assertTrue(audit(envelope(row()))['review_required'])

    def test_processed_pre_change_deferred(self):
        r=self.review(row(processed=processed(last_crawl_at='2026-11-16T00:00:00Z',selected_canonical=B)))
        self.assertEqual(r['processed_recency'],'predates_declared_change')
        self.assertNotIn('processed_selected_canonical_differs_review',r['review_findings'])

    def test_recent_processed_mismatch(self):
        r=self.review(row(processed=processed(state='not_indexed',selected_canonical=B)))
        self.assertIn('processed_selected_canonical_differs_review',r['review_findings'])
        self.assertIn('processed_representative_not_indexed_review',r['review_findings'])

    def test_noindex_and_robots(self):
        r=row()
        r['current'].update(robots='disallowed',http_noindex=True)
        flags=self.review(r)['review_findings']
        self.assertIn('intended_representative_noindex_review',flags)
        self.assertIn('disallow_may_prevent_directive_discovery_review',flags)

    def test_conflicting_declarations(self):
        r=row()
        r['current']['header_canonicals']=[B,B]
        flags=self.review(r)['review_findings']
        self.assertIn('different_canonical_targets_review',flags)
        self.assertIn('multiple_canonical_declarations_review',flags)

    def test_no_canonical_not_universal_failure(self):
        r=row()
        r['current'].update(source_canonicals=[],rendered_canonicals=[])
        self.assertEqual(self.review(r)['review_findings'],[])

    def test_unknown_not_empty(self):
        r=row()
        r['current'].update(status='partial',rendered_canonicals=None,rendered_noindex=None)
        self.assertIn('canonical_groups_incomplete',self.review(r)['deferred_checks'])

    def test_target_outside_inventory(self):
        r=row(intent='duplicate',preferred_url=B)
        r['current'].update(source_canonicals=[B],rendered_canonicals=[B],sitemap_member=False)
        self.assertIn('canonical_target_not_in_supplied_inventory',self.review(r)['deferred_checks'])

    def test_cycle(self):
        a=row(intent='duplicate',preferred_url=B)
        b=row('b',B,intent='duplicate',preferred_url=A)
        for r,target in ((a,B),(b,A)):
            r['current'].update(source_canonicals=[target],rendered_canonicals=[target],sitemap_member=False)
        for r in audit(envelope(a,b))['urls']:
            self.assertIn('canonical_cycle_review',r['review_findings'])

    def test_target_noindex_non200(self):
        a=row(intent='duplicate',preferred_url=B)
        a['current'].update(source_canonicals=[B],rendered_canonicals=[B])
        b=row('b',B)
        b['current'].update(http_status=404,http_noindex=True)
        flags=audit(envelope(a,b))['urls'][0]['review_findings']
        self.assertIn('canonical_target_non_200_review',flags)
        self.assertIn('canonical_target_noindex_review',flags)

    def test_failed_not_observed(self):
        r=row()
        r['current']['status']='failed'
        with self.assertRaises(ValueError): self.review(r)
        r['current'].update(http_status=None,http_noindex=None,initial_noindex=None,rendered_noindex=None,
                            source_canonicals=None,header_canonicals=None,rendered_canonicals=None)
        self.assertIn('current_capture_incomplete',self.review(r)['deferred_checks'])

    def test_invalid_inputs(self):
        for r in (row(u='https://user@example.org/'),row(processed=processed(last_crawl_at='2026-11-19T00:00:00Z')),
                  row(changed_at='2026-02-30T00:00:00Z')):
            with self.assertRaises(ValueError): self.review(r)
        with self.assertRaises(ValueError): audit(envelope(row(),row()))
        d=envelope(row());d['extra']=float('nan')
        with self.assertRaises(ValueError): audit(d)
