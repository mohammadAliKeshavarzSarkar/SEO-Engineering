import unittest
from scripts.audit_locale_manifest import audit


def fixture():
    urls = {'fa': 'https://example.org/fa/guide/', 'en': 'https://example.org/en/guide/'}
    return {'allowed_tags':['fa','en'], 'pages':[
        dict(url=url, group='guide', locale=tag, status=200, index_intent=True,
             canonical=url, alternates=[dict(tag=t,url=u) for t,u in urls.items()])
        for tag,url in urls.items()]}


class LocaleTests(unittest.TestCase):
    def reasons(self, data):
        return {f['reason'] for f in audit(data)['findings']}

    def test_valid(self):
        self.assertEqual(audit(fixture())['findings'], [])

    def test_missing_return(self):
        data = fixture()
        data['pages'][1]['alternates'].pop(0)
        self.assertIn('alternate_set_differs_from_group', self.reasons(data))

    def test_cross_language_canonical(self):
        data = fixture()
        data['pages'][0]['canonical'] = data['pages'][1]['url']
        self.assertIn('non_self_canonical_review', self.reasons(data))

    def test_single_language(self):
        data = fixture()
        data['pages'].pop()
        data['pages'][0]['alternates'] = []
        self.assertEqual(audit(data)['findings'], [])

    def test_redirect_or_noindex(self):
        data = fixture()
        data['pages'][0]['status'] = 301
        data['pages'][1]['index_intent'] = False
        self.assertEqual(len(audit(data)['findings']), 2)

    def test_duplicate_tag(self):
        data = fixture()
        data['pages'][0]['alternates'].append(data['pages'][0]['alternates'][0])
        self.assertIn('duplicate_alternate_tag', self.reasons(data))

    def test_unknown_target(self):
        data = fixture()
        data['pages'][0]['alternates'][1]['url'] = 'https://example.org/missing/'
        self.assertIn('target_not_in_manifest', self.reasons(data))

    def test_case_insensitive_tag(self):
        data = fixture()
        data['pages'][0]['alternates'][0]['tag'] = 'FA'
        self.assertEqual(audit(data)['findings'], [])

    def test_invalid_project_tag(self):
        data = fixture()
        data['allowed_tags'] = ['fa', 'IR-123']
        with self.assertRaises(ValueError):
            audit(data)
