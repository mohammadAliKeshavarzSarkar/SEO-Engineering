import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile, ZipInfo
from scripts.build_skill import build, LIBRARY_DIRS
from scripts.verify_package import verify


class VerifyPackageTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        for base in LIBRARY_DIRS:
            self.write(f'{base}/demo.md', 'demo')
        self.write('skills/seo-engineering/SKILL.md',
                   '---\nname: seo-engineering\ndescription: Test SEO skill\n---\n# Skill\n')
        self.write('skills/seo-engineering/references/router.md', 'router')
        self.write('skills/seo-engineering/references/execution-contract.md', 'contract')
        for name in ('audit_html.py','check_docs.py','cluster_keywords.py','audit_topic_graph.py',
                     'prioritize_opportunities.py','audit_locale_manifest.py','validate_research.py','inspect_architecture.py','audit_rendering.py','audit_spa_build.py','README.md'):
            self.write('scripts/' + name, 'demo')
        self.archive = self.root / 'skill.zip'

    def write(self, path, content):
        p = self.root / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding='utf-8')

    def test_verified_receipt(self):
        count = build(self.root, self.archive)
        report = verify(self.root, self.archive)
        self.assertEqual(report['file_count'], count)
        self.assertEqual(len(report['archive_sha256']), 64)
        self.assertEqual(report['runtime_activation'], 'not_tested')
        self.assertTrue(all(len(r['sha256']) == 64 for r in report['files']))

    def test_stale_source_same_length(self):
        build(self.root, self.archive)
        self.write('docs/demo.md', 'evil')
        with self.assertRaisesRegex(ValueError, 'content mismatch'):
            verify(self.root, self.archive)

    def test_extra_member(self):
        build(self.root, self.archive)
        with ZipFile(self.archive, 'a') as z:
            z.writestr('seo-engineering/extra.md', 'extra')
        with self.assertRaisesRegex(ValueError, 'membership'):
            verify(self.root, self.archive)

    def test_duplicate_or_case_collision(self):
        self.write('docs/DEMO.md', 'other')
        build(self.root, self.archive)
        with self.assertRaisesRegex(ValueError, 'case-colliding'):
            verify(self.root, self.archive)

    def test_nested_skill(self):
        self.write('docs/SKILL.md', 'extra skill')
        build(self.root, self.archive)
        with self.assertRaisesRegex(ValueError, 'exactly one'):
            verify(self.root, self.archive)

    def test_wrong_name(self):
        self.write('skills/seo-engineering/SKILL.md', '---\nname: wrong\ndescription: Test\n---\n')
        build(self.root, self.archive)
        with self.assertRaisesRegex(ValueError, 'frontmatter'):
            verify(self.root, self.archive)

    def test_unsafe_member_type(self):
        build(self.root, self.archive)
        altered = self.root / 'altered.zip'
        with ZipFile(self.archive) as original, ZipFile(altered, 'w') as out:
            for i in original.infolist():
                data = original.read(i)
                if i.filename.endswith('/docs/demo.md'):
                    i.external_attr = 0o120777 << 16
                out.writestr(i, data)
        with self.assertRaisesRegex(ValueError, 'unsafe archive member'):
            verify(self.root, altered)
