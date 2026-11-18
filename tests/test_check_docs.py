import tempfile
import unittest
from pathlib import Path
from scripts.check_docs import audit


class DocsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)

    def write(self, path, content):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')

    def layout(self, portable=False):
        skill = self.base / ('seo-engineering' if portable else 'skills/seo-engineering')
        root = skill / 'references/library' if portable else self.base
        self.write(skill / 'SKILL.md', '[router](references/router.md)')
        self.write(skill / 'references/router.md', 'Load docs/guide.md; templates/test.csv')
        self.write(skill / 'references/execution-contract.md', 'Contract')
        self.write(root / 'docs/guide.md', '[template](../templates/test.csv)')
        self.write(root / 'templates/test.csv', 'id\n')
        return root, skill

    def test_repository(self):
        root, _ = self.layout()
        self.assertEqual(audit(root), (4, 2, []))

    def test_portable(self):
        root, _ = self.layout(True)
        self.assertEqual(audit(root), (4, 2, []))

    def test_missing_router_resource(self):
        root, skill = self.layout()
        self.write(skill / 'references/router.md', 'Load docs/missing.md')
        self.assertIn('skill routing: docs/missing.md', audit(root)[2])

    def test_portable_entry_link(self):
        root, skill = self.layout(True)
        self.write(skill / 'SKILL.md', '[missing](references/absent.md)')
        self.assertIn('SKILL.md: references/absent.md', audit(root)[2])

    def test_missing_contract(self):
        root, skill = self.layout()
        (skill / 'references/execution-contract.md').unlink()
        self.assertTrue(any('execution-contract.md' in e for e in audit(root)[2]))

    def test_escape(self):
        root, _ = self.layout(True)
        self.write(self.base / 'outside.md', 'outside')
        self.write(root / 'docs/guide.md', '[outside](../../../../outside.md)')
        self.assertTrue(audit(root)[2])

    def test_external_and_fenced_links(self):
        root, _ = self.layout()
        self.write(root / 'docs/guide.md', '[remote](https://example.org/)\n```md\n[x](missing.md)\n```')
        self.assertFalse(audit(root)[2])
