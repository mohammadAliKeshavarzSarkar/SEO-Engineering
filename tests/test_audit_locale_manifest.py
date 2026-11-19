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

    def test_language_and_default_alias_require_profile_review(self):
        data = fixture()
        data['allowed_tags'].append('fa-IR')
        data['pages'][0]['locale'] = 'fa-IR'
        for page in data['pages']:
            page['alternates'][0]['tag'] = 'fa-IR'
            page['alternates'].append(dict(tag='fa', url=data['pages'][0]['url']))
            page['alternates'].append(dict(tag='x-default', url=data['pages'][1]['url']))
        findings = audit(data)['findings']
        self.assertEqual({f['reason'] for f in findings}, {'alternate_set_differs_from_group'})
        self.assertEqual(len(findings), 2)

    def test_partial_reciprocal_set_is_strict_profile_finding(self):
        data = fixture()
        data['allowed_tags'].append('de')
        url = 'https://example.org/de/guide/'
        fa, en = data['pages']
        fa['alternates'].append(dict(tag='de', url=url))
        data['pages'].append(dict(url=url, group='guide', locale='de', status=200,
             index_intent=True, canonical=url, alternates=[dict(tag='fa',url=fa['url']),dict(tag='de',url=url)]))
        findings = audit(data)['findings']
        self.assertEqual({f['reason'] for f in findings}, {'alternate_set_differs_from_group'})
        self.assertEqual({f['url'] for f in findings}, {en['url'],url})

    def test_tag_shape_does_not_validate_official_codes(self):
        data = fixture()
        data['allowed_tags'] = ['fa','zz-UK']
        data['pages'][1]['locale'] = 'zz-UK'
        for page in data['pages']:
            page['alternates'][1]['tag'] = 'zz-UK'
        self.assertEqual(audit(data)['findings'], [])
