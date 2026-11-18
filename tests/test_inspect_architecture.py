import unittest
from scripts.inspect_architecture import summarize


def route(**changes):
    r = dict(id='guide',expected='public',declared_strategy='unknown',status=200,
             source_content='present',rendered_content='present',initial_noindex=False,
             rendered_noindex=False,unauthorized_content_visible=None,evidence_ref='synthetic')
    r.update(changes)
    return r


def fixture(*routes):
    return dict(schema_version='1',scope='synthetic',declared_dependencies={'vite':'^7','react':'^19'},
                routes=list(routes))


class ArchitectureTests(unittest.TestCase):
    def row(self, **changes):
        return summarize(fixture(route(**changes)))['routes'][0]

    def test_framework_not_mode(self):
        report = summarize(fixture(route()))
        self.assertEqual(len(report['dependency_hints']),2)
        self.assertEqual(report['routes'][0]['declared_strategy'],'unknown')
        self.assertEqual(report['routes'][0]['delivery_observation'],'initial_content_observed')

    def test_client_completion(self):
        self.assertEqual(self.row(source_content='absent')['delivery_observation'],'client_completion_observed')

    def test_both_incomplete(self):
        self.assertIn('investigate_missing_primary_content',self.row(source_content='partial',rendered_content='absent')['findings'])

    def test_initial_noindex(self):
        self.assertIn('initial_noindex_removed_after_render',self.row(initial_noindex=True)['findings'])

    def test_private_not_acquisition(self):
        r = self.row(expected='private',status=200,unauthorized_content_visible=True)
        self.assertEqual(r['delivery_observation'],'not_assessed')
        self.assertIn('suspected_private_content_exposure_escalate',r['findings'])

    def test_missing_route(self):
        self.assertIn('missing_route_status_review',self.row(expected='missing')['findings'])
        self.assertEqual(self.row(expected='missing',status=404)['findings'],[])

    def test_unknown_not_failure(self):
        r = self.row(status=None,source_content='unknown',rendered_content='unknown')
        self.assertEqual(r['delivery_observation'],'not_assessed')
        self.assertIn('public_status_unknown',r['findings'])

    def test_render_regression(self):
        self.assertIn('content_regression_after_render',self.row(rendered_content='partial')['findings'])

    def test_invalid_values_and_ids(self):
        for data in (fixture(route(status=True)),fixture(route(initial_noindex='false')),
                     fixture(route(source_content='yes')),fixture(route(),route())):
            with self.assertRaises(ValueError): summarize(data)
