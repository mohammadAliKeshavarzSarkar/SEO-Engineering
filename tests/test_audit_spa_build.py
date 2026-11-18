import tempfile
import unittest
from pathlib import Path
from scripts.audit_spa_build import audit


def route(**changes):
    row = dict(id='guide',url='https://example.org/guide/',purpose='acquisition',
               delivery='prerendered',sitemap_expected=True,
               canonical_expected='https://example.org/guide/',
               html_file='guide/index.html',required_files=['guide/data.json'])
    row.update(changes)
    return row


def plan(*routes):
    return dict(schema_version='1',scope='synthetic',routes=list(routes))


class SpaBuildTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.write('guide/index.html','<html>fixture</html>')
        self.write('guide/data.json','{}')
        self.write('shell.html','<html>shell</html>')

    def write(self, name, text):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding='utf-8')
        return p

    def row(self, **changes):
        return audit(plan(route(**changes)),self.root)['routes'][0]

    def test_present_not_deployment_pass(self):
        r = self.row()
        self.assertEqual(r['review_findings'],[])
        self.assertIn('deployed_routing_headers_and_status_not_checked',r['deferred_checks'])
        self.assertTrue(audit(plan(route()),self.root)['review_required'])

    def test_missing_and_empty(self):
        (self.root/'guide/data.json').unlink()
        self.write('guide/index.html','')
        self.assertEqual(self.row()['review_findings'],['required_artifact_empty','required_artifact_missing'])

    def test_dynamic_runtime_not_missing_html(self):
        r = self.row(delivery='runtime',html_file=None,required_files=[])
        self.assertEqual(r['review_findings'],[])
        self.assertIn('runtime_document_not_assessed',r['deferred_checks'])

    def test_shared_shell_and_static_collision(self):
        a = route(delivery='spa_shell',html_file='shell.html',required_files=[])
        b = route(id='catalog',url='https://example.org/catalog/',delivery='spa_shell',
                  html_file='shell.html',required_files=[],sitemap_expected=False)
        self.assertTrue(all(not r['review_findings'] for r in audit(plan(a,b),self.root)['routes']))
        b['delivery']='prerendered'
        self.assertTrue(all('document_path_collision_review' in r['review_findings'] for r in audit(plan(a,b),self.root)['routes']))

    def test_missing_route_fallback(self):
        r=self.row(purpose='missing',delivery='spa_shell',html_file='shell.html',required_files=[],sitemap_expected=False)
        self.assertIn('missing_route_fallback_status_review',r['review_findings'])

    def test_protected_plan(self):
        r=self.row(purpose='protected')
        self.assertIn('protected_route_prerender_plan_review',r['review_findings'])
        self.assertIn('non_acquisition_route_in_sitemap_plan',r['review_findings'])

    def test_unknown_and_conflicting_canonical(self):
        self.assertIn('sitemap_canonical_expectation_unknown',self.row(canonical_expected=None)['deferred_checks'])
        self.assertIn('sitemap_non_self_canonical_plan_review',self.row(canonical_expected='https://example.org/')['review_findings'])

    def test_explicit_unicode_path(self):
        self.write('راهنما/index.html','fixture')
        r=self.row(url='https://example.org/%D8%B1/',html_file='راهنما/index.html',required_files=[],sitemap_expected=False)
        self.assertEqual(r['artifact_checks'][0]['state'],'present')

    def test_unsafe_paths(self):
        for path in ('../secret.html','/abs.html','C:/x.html','guide/../../secret.html','guide\\index.html','guide/.hidden.html'):
            with self.assertRaises(ValueError): self.row(html_file=path)

    def test_symlink_ancestor(self):
        (self.root/'alias').symlink_to(self.root/'guide',target_is_directory=True)
        with self.assertRaises(ValueError): self.row(html_file='alias/index.html',required_files=[])

    def test_invalid_and_duplicate_records(self):
        for row in (route(sitemap_expected='true'),route(url='https://user@example.org/'),route(delivery='runtime'),
                    route(required_files=['guide/data.json','GUIDE/DATA.JSON'])):
            with self.assertRaises(ValueError): audit(plan(row),self.root)
        with self.assertRaises(ValueError): audit(plan(route(),route()),self.root)

    def test_directory_is_not_artifact(self):
        (self.root/'folder.html').mkdir()
        self.assertIn('required_artifact_not_regular',self.row(html_file='folder.html')['review_findings'])
