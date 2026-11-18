import copy
import unittest
from scripts.audit_rendering import audit


def capture(**updates):
    row = dict(status='complete',context_id='fixture-deployment-mobile-en',
               evidence_ref='fixture',primary_content='present',
               titles=['Example'],canonicals=['https://example.org/guide/'],
               meta_noindex=False,link_targets=['home','catalog'])
    row.update(updates)
    return row


def pair(**updates):
    row = dict(id='guide',index_intent=True,http_status=200,http_noindex=False,
               comparability='matched',readiness='met',required_link_targets=['catalog'],
               source=capture(evidence_ref='source'),rendered=capture(evidence_ref='dom'))
    row.update(updates)
    return row


def envelope(*routes):
    return dict(schema_version='1',scope='synthetic',routes=list(routes))


class RenderingTests(unittest.TestCase):
    def row(self, **updates):
        return audit(envelope(pair(**updates)))['routes'][0]

    def test_matched_healthy(self):
        result = self.row()
        self.assertEqual(result['paired_comparison'],'performed')
        self.assertEqual(result['review_findings'],[])
        self.assertEqual(result['deferred_checks'],[])
        self.assertTrue(audit(envelope(pair()))['review_required'])

    def test_client_completion_not_index_failure(self):
        result = self.row(source=capture(primary_content='absent'))
        self.assertEqual(result['review_findings'],['client_completion_review'])

    def test_content_regression(self):
        result = self.row(rendered=capture(primary_content='partial'))
        self.assertIn('primary_content_regression_review',result['review_findings'])

    def test_initial_and_http_noindex_independent(self):
        result = self.row(http_noindex=True,source=capture(meta_noindex=True))
        self.assertIn('applicable_http_noindex_review',result['review_findings'])
        self.assertIn('initial_meta_noindex_review',result['review_findings'])
        self.assertIn('initial_meta_noindex_absent_after_render',result['review_findings'])

    def test_nonindex_intent_not_initial_error(self):
        result = self.row(index_intent=False,http_noindex=True,source=capture(meta_noindex=True))
        self.assertNotIn('applicable_http_noindex_review',result['review_findings'])
        self.assertNotIn('initial_meta_noindex_review',result['review_findings'])

    def test_metadata_and_link_change(self):
        result = self.row(rendered=capture(canonicals=['different','another'],titles=['New'],link_targets=['home']))
        for flag in ('canonicals_changed_review','titles_changed_review',
                     'rendered_multiple_canonical_declarations_review',
                     'source_link_targets_not_in_render_review','required_link_targets_missing_from_render_review'):
            self.assertIn(flag,result['review_findings'])

    def test_unperformed_render_no_absence(self):
        dom = capture(status='not_collected',evidence_ref=None,primary_content='unknown',
                      titles=None,canonicals=None,meta_noindex=None,link_targets=None)
        result = self.row(rendered=dom,readiness='unknown')
        self.assertEqual(result['paired_comparison'],'not_performed')
        self.assertEqual(result['review_findings'],[])
        self.assertIn('rendered_capture_incomplete',result['deferred_checks'])

    def test_partial_and_timeout_never_assert_loss(self):
        for changes in (dict(rendered=capture(status='partial',primary_content='absent')),
                        dict(readiness='not_met',rendered=capture(primary_content='absent')),
                        dict(comparability='unknown',rendered=capture(primary_content='absent'))):
            result = self.row(**changes)
            self.assertEqual(result['paired_comparison'],'not_performed')
            self.assertNotIn('primary_content_regression_review',result['review_findings'])

    def test_unknown_fields_not_empty(self):
        result = self.row(rendered=capture(canonicals=None,link_targets=None,primary_content='unknown'))
        self.assertIn('canonicals_comparison_unavailable',result['deferred_checks'])
        self.assertIn('required_link_target_check_unavailable',result['deferred_checks'])
        self.assertNotIn('canonicals_changed_review',result['review_findings'])

    def test_context_mismatch_and_invalid_types(self):
        for row in (pair(rendered=capture(context_id='different')),pair(http_status=True),
                    pair(http_noindex='false'),pair(http_status=None),pair(index_intent=1)):
            with self.assertRaises(ValueError): audit(envelope(row))

    def test_failed_capture_cannot_assert_values(self):
        with self.assertRaises(ValueError):
            audit(envelope(pair(rendered=capture(status='failed'))))

    def test_duplicate_and_nonfinite(self):
        with self.assertRaises(ValueError): audit(envelope(pair(),pair()))
        data = envelope(pair())
        data['extra'] = float('nan')
        with self.assertRaises(ValueError): audit(data)
