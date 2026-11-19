import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile, ZipInfo
from scripts.build_skill import build, LIBRARY_DIRS
from scripts.verify_package import verify, verify_installed, portable_paths


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
                     'prioritize_opportunities.py','audit_locale_manifest.py','validate_research.py','inspect_architecture.py','audit_rendering.py','audit_spa_build.py','audit_next_delivery.py','audit_crawl_evidence.py','audit_index_evidence.py','audit_migration.py','audit_metadata.py','audit_performance.py','audit_technical.py','review_release_gates.py','review_incident.py','README.md'):
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

    def installed(self):
        build(self.root, self.archive)
        receipt = verify(self.root, self.archive)
        target = self.root / "independent project" / ".agents" / "skills"
        target.mkdir(parents=True)
        with ZipFile(self.archive) as z:
            z.extractall(target)
        return target / "seo-engineering", receipt

    def test_installed_exact_membership(self):
        target, receipt = self.installed()
        result = verify_installed(target, receipt)
        self.assertEqual(result["file_count"], receipt["file_count"])
        self.assertEqual(result["status"], "source_matched")
        self.assertEqual(result["runtime_activation"], "not_tested")

    def test_installed_modified_same_length(self):
        target, receipt = self.installed()
        (target / "references/library/docs/demo.md").write_text("evil")
        with self.assertRaisesRegex(ValueError, "content mismatch"):
            verify_installed(target, receipt)

    def test_missing_installed_resource(self):
        target, receipt = self.installed()
        (target / "references/router.md").unlink()
        with self.assertRaisesRegex(ValueError, "membership mismatch"):
            verify_installed(target, receipt)

    def test_extra_installed_file_and_directory(self):
        target, receipt = self.installed()
        extra = target / "extra.md"
        extra.write_text("not reviewed")
        with self.assertRaisesRegex(ValueError, "unexpected installation file"):
            verify_installed(target, receipt)
        extra.unlink()
        extra = target / "empty-directory"
        extra.mkdir()
        with self.assertRaisesRegex(ValueError, "unexpected installation directory"):
            verify_installed(target, receipt)

    def test_installed_symlink_rejected(self):
        target, receipt = self.installed()
        p = target / "references/router.md"
        p.unlink()
        p.symlink_to(self.root / "skills/seo-engineering/references/router.md")
        with self.assertRaisesRegex(ValueError, "unsafe installation file"):
            verify_installed(target, receipt)

    def test_installed_directory_symlink_rejected(self):
        target, receipt = self.installed()
        (target / "elsewhere").symlink_to(self.root / "docs", target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "unsafe installation directory"):
            verify_installed(target, receipt)

    def test_portability_directory_prefix_collisions(self):
        for names in (["seo-engineering/docs/a.md", "seo-engineering/DOCS/b.md"],
                      ["seo-engineering/café/a.md", "seo-engineering/cafe\u0301/b.md"],
                      ["seo-engineering/docs", "seo-engineering/docs/b.md"]):
            with self.subTest(names=names), self.assertRaises(ValueError):
                portable_paths(names)

    def test_portability_reserved_components(self):
        for path in ("CON.md", "folder./file.md", "LPT1.txt", "bad:name.md", "a\\\\b.md"):
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, "nonportable"):
                portable_paths(["seo-engineering/" + path])

    def test_duplicate_skill_name(self):
        self.write("skills/seo-engineering/SKILL.md",
                   "---\nname: seo-engineering\nname: different\ndescription: Test\n---\n")
        build(self.root, self.archive)
        with self.assertRaisesRegex(ValueError, "frontmatter"):
            verify(self.root, self.archive)
