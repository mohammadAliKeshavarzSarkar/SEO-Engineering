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
