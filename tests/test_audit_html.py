import tempfile
import unittest
from pathlib import Path
from scripts.audit_html import audit

class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.url = 'https://example.org/'
        self.route = {'url': self.url, 'file': 'index.html'}
        self.good = '<html><head><title>Example</title><meta name="description" content="Example summary"><link rel="canonical" href="https://example.org/"></head><body><h1>Example</h1></body></html>'
    def run_html(self, content):
        (self.root/'index.html').write_text(content, encoding='utf-8')
        return audit([self.route], self.root)
    def test_good(self):
        self.assertEqual(self.run_html(self.good), [])
    def test_wrong_canonical(self):
        self.assertTrue(any('canonical mismatch' in x for x in self.run_html(self.good.replace(self.url, 'https://example.org/wrong'))))
    def test_noindex(self):
        self.assertTrue(any('noindex' in x for x in self.run_html(self.good.replace('</head>', '<meta name="robots" content="noindex,follow"></head>'))))
    def test_missing(self):
        self.assertTrue(any('missing HTML' in x for x in audit([self.route], self.root)))
    def test_duplicate_headings(self):
        self.assertTrue(any('h1' in x for x in self.run_html(self.good.replace('</body>', '<h1>Extra</h1></body>'))))
    def test_empty(self):
        self.assertTrue(audit([], self.root))
    def test_path_escape(self):
        self.assertTrue(any('escapes root' in x for x in audit([{'url':self.url, 'file':'../index.html'}], self.root)))
    def test_duplicate_metadata(self):
        (self.root/'index.html').write_text(self.good, encoding='utf-8')
        url2 = self.url+'second'
        (self.root/'second.html').write_text(self.good.replace(self.url, url2), encoding='utf-8')
        result = audit([self.route, {'url':url2, 'file':'second.html'}], self.root)
        self.assertTrue(any('duplicate title' in x for x in result))
        self.assertTrue(any('duplicate description' in x for x in result))

    def test_svg_title_not_document_title(self):
        self.assertEqual(self.run_html(self.good.replace('</body>', '<svg><title>Icon</title></svg></body>')), [])

    def test_inert_template_metadata(self):
        html = self.good.replace('</body>', '<template><h1>Draft</h1><link rel="canonical" href="https://example.org/draft"></template></body>')
        self.assertEqual(self.run_html(html), [])

    def test_body_canonical_rejected(self):
        html = self.good.replace('</body>', '<link rel="canonical" href="https://example.org/"></body>')
        self.assertTrue(any('outside explicit head' in x for x in self.run_html(html)))

    def test_body_noindex_still_detected(self):
        html = self.good.replace('</body>', '<meta name="robots" content="noindex"></body>')
        self.assertTrue(any('noindex' in x for x in self.run_html(html)))

    def test_indexable_boolean_required(self):
        for value in ('false', 0, None):
            with self.assertRaises(ValueError):
                audit([dict(self.route, indexable=value)], self.root)

    def test_invalid_route_url(self):
        for url in ('/relative', 'https://user:pass@example.org/', 'https://example.org/#part', 'https://example.org:bad/'):
            with self.assertRaises(ValueError):
                audit([dict(self.route, url=url)], self.root)

    def test_invalid_manifest_shape(self):
        with self.assertRaises(ValueError):
            audit({'url':self.url, 'file':'index.html'}, self.root)
