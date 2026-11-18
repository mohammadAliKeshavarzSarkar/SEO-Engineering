import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile
from scripts.build_skill import build, collect, LIBRARY_DIRS


class BuildSkillTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for base in LIBRARY_DIRS:
            self.write(f'{base}/demo.md', 'demo')
        self.write('skills/seo-engineering/SKILL.md', 'skill')
        self.write('skills/seo-engineering/references/router.md', 'router')
        self.write('scripts/audit_html.py', '# audit')
        self.write('scripts/check_docs.py', '# check')
        self.write('scripts/cluster_keywords.py', '# cluster')
        self.write('scripts/audit_topic_graph.py', '# graph')
        self.write('scripts/prioritize_opportunities.py', '# prioritize')

    def write(self, name, content):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding='utf-8')
        return p

    def test_bundle_and_private_exclusion(self):
        for p in ('private/secret.md', 'projects/beatfit/audit.md', 'docs/private/secret.md',
                  'docs/.env', 'docs/__pycache__/x.py', 'scripts/unapproved.py'):
            self.write(p, 'not for distribution')
        out = self.root / 'package.zip'
        count = build(self.root, out)
        with ZipFile(out) as z:
            names = set(z.namelist())
            self.assertEqual(count, len(names))
            self.assertIn('seo-engineering/SKILL.md', names)
            self.assertIn('seo-engineering/references/library/scripts/cluster_keywords.py', names)
            self.assertIn('seo-engineering/references/library/scripts/audit_topic_graph.py', names)
            self.assertIn('seo-engineering/references/library/scripts/prioritize_opportunities.py', names)
            self.assertIn('seo-engineering/references/library/docs/demo.md', names)
            self.assertFalse(any(b'not for distribution' in z.read(n) for n in names))
            self.assertIsNone(z.testzip())

    def test_no_overwrite(self):
        out = self.write('package.zip', 'keep')
        with self.assertRaises(FileExistsError):
            build(self.root, out)
        self.assertEqual(out.read_text(), 'keep')

    def test_symlink_rejected(self):
        secret = self.write('private/secret.md', 'secret')
        (self.root / 'docs/link.md').symlink_to(secret)
        with self.assertRaises(ValueError):
            collect(self.root)

    def test_missing_resource(self):
        (self.root / 'skills/seo-engineering/SKILL.md').unlink()
        with self.assertRaises(ValueError):
            collect(self.root)
