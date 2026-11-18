import unittest
from scripts.audit_migration import audit

A='https://old.example.org/a/'
B='https://new.example.org/b/'
C='https://new.example.org/c/'


def tx(u,s,t=None):
    return dict(url=u,status=s,resolved_location=t,evidence_ref='fixture:transaction')


def route(ident='a',u=A,t=B,**kw):
    r=dict(id=ident,old_url=u,action='permanent_redirect',target_url=t,
           plan_ref='fixture:map',replacement_reviewed=True,terminal_statuses=[200],
           trace=dict(status='complete',context_matched=True,evidence_ref='fixture:trace',
                      transactions=[tx(u,301,t),tx(t,200)]))
    r.update(kw)
    return r


def trace(*hops,status='partial',matched=True):
    return dict(status=status,context_matched=matched,evidence_ref='fixture:trace',transactions=list(hops))


def envelope(*rows):
    return dict(schema_version='1',scope='synthetic',policy_version='fixture-1',
                allowed_origins=['https://old.example.org','https://new.example.org'],routes=list(rows))


class MigrationTests(unittest.TestCase):
    def row(self,**kw):
        return audit(envelope(route(**kw)))['routes'][0]

    def test_direct_not_search_proof(self):
        r=audit(envelope(route()))
        self.assertTrue(r['review_required'])
        self.assertEqual(r['routes'][0]['review_findings'],[])

    def test_wrong_redirect_type(self):
        r=self.row(trace=trace(tx(A,302,B),tx(B,200),status='complete'))
        self.assertIn('permanent_redirect_status_mismatch_review',r['review_findings'])

    def test_parameter_loss_exact_match(self):
        t=B+'?size=large&size=small'
        r=self.row(t=t,trace=trace(tx(A,301,B),tx(B,200),status='complete'))
        self.assertIn('terminal_url_differs_from_reviewed_mapping',r['review_findings'])

    def test_wrong_terminal_status(self):
        r=self.row(trace=trace(tx(A,301,B),tx(B,404),status='complete'))
        self.assertIn('terminal_status_differs_from_expectation',r['review_findings'])

    def test_chain(self):
        r=self.row(trace=trace(tx(A,301,C),tx(C,301,B),tx(B,200),status='complete'))
        self.assertIn('observed_multiple_redirect_hops_review',r['review_findings'])

    def test_observed_loop(self):
        r=self.row(trace=trace(tx(A,301,B),tx(B,301,A)))
        self.assertIn('observed_redirect_cycle_review',r['review_findings'])
        self.assertIn('terminal_response_unverified',r['deferred_checks'])

    def test_planned_cycle(self):
        result=audit(envelope(route(),route('b',B,A)))
        for r in result['routes']:
            self.assertIn('planned_redirect_cycle_review',r['review_findings'])

    def test_partial_and_wrong_context(self):
        r=self.row(trace=trace(tx(A,301,B),matched=False))
        self.assertIn('trace_context_not_established',r['deferred_checks'])
        self.assertIn('terminal_response_unverified',r['deferred_checks'])
        self.assertNotIn('terminal_url_differs_from_reviewed_mapping',r['review_findings'])

    def test_outside_scope_destination(self):
        r=self.row(trace=trace(tx(A,301,'https://outside.example.org/')))
        self.assertIn('observed_redirect_outside_approved_origins_review',r['review_findings'])
        with self.assertRaises(ValueError): self.row(t='https://outside.example.org/')

    def test_removed_no_replacement(self):
        r=self.row(action='remove',target_url=None,replacement_reviewed=None,terminal_statuses=[404,410],
                   trace=trace(tx(A,410),status='complete'))
        self.assertEqual(r['review_findings'],[])

    def test_uncollected(self):
        r=self.row(trace=dict(status='not_collected',context_matched=None,evidence_ref=None,transactions=[]))
        self.assertIn('terminal_response_unverified',r['deferred_checks'])

    def test_invalid_chain_and_304(self):
        for hops in (trace(tx(A,301,B),tx(C,200),status='complete'),trace(tx(A,304),status='complete'),
                     trace(tx(A,301,B),status='complete')):
            with self.assertRaises(ValueError): self.row(trace=hops)
        with self.assertRaises(ValueError): self.row(terminal_statuses=[304])

    def test_invalid_urls_and_duplicate_records(self):
        for u in ('https://user@old.example.org/a/','https://old.example.org/a#x','https://old.example.org/%xy','https://old.example.org:0/a/'):
            with self.assertRaises(ValueError): self.row(u=u)
        with self.assertRaises(ValueError): audit(envelope(route(),route()))

    def test_unicode_and_encoded_reserved_not_equivalent(self):
        t='https://new.example.org/راهنما/%2F'
        r=self.row(t=t,trace=trace(tx(A,301,t),tx(t,200),status='complete'))
        self.assertEqual(r['review_findings'],[])
        r=self.row(t=t,trace=trace(tx(A,301,t.replace('%2F','/')),tx(t.replace('%2F','/'),200),status='complete'))
        self.assertIn('terminal_url_differs_from_reviewed_mapping',r['review_findings'])
