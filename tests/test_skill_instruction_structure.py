"""Text/packaging regressions only; not instruction-compliance or agent tests."""
import re
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from scripts.build_skill import build
from scripts.check_docs import audit

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/seo-engineering"


class InstructionStructureTests(unittest.TestCase):
    def test_entry_editorial_budget(self):
        entry = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertLessEqual(len(entry.split()), 450)
        self.assertIn("[execution contract](references/execution-contract.md)", entry)
        self.assertIn("[task router](references/router.md)", entry)

    def test_router_keeps_evaluation_route_explicitly_maintainer_only(self):
        router = (SKILL / "references/router.md").read_text(encoding="utf-8")
        rows = [line for line in router.splitlines() if line.startswith("| ")]
        evaluation_rows = [row for row in rows if re.search(r"\bevaluations/", row)]
        self.assertEqual(len(evaluation_rows), 1)
        self.assertTrue(evaluation_rows[0].startswith("| Maintainer-only:"))

    def test_instruction_resources_in_fresh_package(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            archive = base / "candidate.zip"
            build(ROOT, archive)
            with ZipFile(archive) as bundle:
                for relative in ("SKILL.md", "references/router.md", "references/execution-contract.md"):
                    self.assertEqual(bundle.read("seo-engineering/" + relative),
                                     (SKILL / relative).read_bytes())
                bundle.extractall(base / "installed")
            lib = base / "installed/seo-engineering/references/library"
            self.assertEqual(audit(lib)[2], [])
            self.assertFalse((base / "installed/seo-engineering/AGENTS.md").exists())


if __name__ == "__main__":
    unittest.main()
