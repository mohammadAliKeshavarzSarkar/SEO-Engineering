"""Historical fixture inventory and practice plan integrity, not project execution."""
import json
import re
import unittest
from pathlib import Path

from scripts.build_skill import collect

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "operations/ts08-example-coverage.json"


class PracticeInventoryTests(unittest.TestCase):
    def setUp(self):
        self.record = json.loads(INVENTORY.read_text(encoding="utf-8"))

    def test_baseline_inventory_paths_and_packaging(self):
        packaged = collect(ROOT)
        all_files = []
        ids = set()
        for family in self.record["families"]:
            self.assertNotIn(family["id"], ids)
            ids.add(family["id"])
            self.assertTrue(family["files"])
            for ref in family["files"]:
                self.assertTrue(ref.startswith("examples/"))
                self.assertIn("seo-engineering/references/library/" + ref, packaged)
                self.assertTrue((ROOT / ref).is_file())
                all_files.append(ref)
        self.assertEqual(len(set(all_files)), len(all_files))
        self.assertEqual(self.record["examples_file_count"], len(all_files))
        # This is a pinned historical inventory, not a restriction on adding new projects.
        self.assertIn("examples/routes-failing.json", all_files)
        self.assertIn("examples/technical-audit/adverse.json", all_files)
        self.assertNotIn("seo-engineering/references/library/operations/ts08-example-coverage.json", packaged)

    def test_planned_projects_use_known_routes_and_existing_examples(self):
        router = (ROOT / "skills/seo-engineering/references/router.md").read_text(encoding="utf-8")
        routes = {row.split("|")[2].strip() for row in router.splitlines()
                  if row.startswith("| ") and len(row.split("|")) == 5
                  and re.fullmatch(r"[A-Z][A-Z0-9_]*", row.split("|")[2].strip())}
        family_ids = {f["id"] for f in self.record["families"]}
        seen = set()
        for project in self.record["projects"]:
            self.assertNotIn(project["id"], seen)
            seen.add(project["id"])
            self.assertEqual(project["state"], "planned")
            self.assertTrue(project["reuse"] and set(project["reuse"]) <= family_ids)
            self.assertTrue(project["routes"] and set(project["routes"]) <= routes)
            self.assertTrue(project["objective"].strip())
        self.assertEqual(seen, {"P01", "P02", "P03", "P04", "P05"})

    def test_practice_guide_portable_and_explicit_scope(self):
        ref = "examples/practice-projects/README.md"
        self.assertIn("seo-engineering/references/library/" + ref, collect(ROOT))
        text = (ROOT / ref).read_text(encoding="utf-8")
        self.assertIn("P03–P05 are planned, not yet implemented", text)
        self.assertIn("not a shared provider schema", text)
        self.assertIn("not just existence of a report", text)


if __name__ == "__main__":
    unittest.main()
