"""Validate authored route catalogue and case references, not agent decisions."""
import json
import re
import unittest
from pathlib import Path

from scripts.build_skill import collect

ROOT = Path(__file__).resolve().parents[1]
ROUTER = ROOT / "skills/seo-engineering/references/router.md"
CASES = ROOT / "operations/ts07-routing-cases.json"
ID = re.compile(r"^[A-Z][A-Z0-9_]*$")
RESOURCE = re.compile(r"^(?:docs|templates|decision-engine|workflows|implementation-patterns|evaluations|scripts)/[\w./-]+\.(?:md|py|csv|json)$")


def read_routes():
    content = ROUTER.read_text(encoding="utf-8")
    section = content.split("| Task or trigger | ID | Reference candidates relative to L |", 1)[1]
    lines = section.strip().splitlines()
    if lines[0] != "|---|---|---|":
        raise ValueError("unexpected route header")
    routes = {}
    for row in lines[1:]:
        if not row.startswith("| "):
            break
        label, ident, raw = [cell.strip() for cell in row[1:-1].split("|")]
        if not ID.fullmatch(ident) or ident in routes:
            raise ValueError("invalid or duplicate route ID")
        refs = [p for p in raw.split("; ") if RESOURCE.fullmatch(p)]
        if not refs or len(refs) != len(set(refs)):
            raise ValueError("invalid resource list")
        routes[ident] = (label, refs)
    return routes


class TaskRouterTests(unittest.TestCase):
    def test_catalogue_covers_specialized_modules(self):
        routes = read_routes()
        self.assertEqual(len(routes), 37)
        self.assertTrue({f"R{i:02}" for i in range(2, 11)} <= set(routes))
        self.assertTrue({f"T{i:02}" for i in range(1, 13)} <= set(routes))
        self.assertIn("ONBOARD", routes)

    def test_all_route_resources_packaged(self):
        packaged = collect(ROOT)
        for ident, (_, refs) in read_routes().items():
            for ref in refs:
                with self.subTest(route=ident, resource=ref):
                    self.assertIn("seo-engineering/references/library/" + ref, packaged)
                    self.assertTrue((ROOT / ref).is_file())

    def test_evaluation_references_only_in_maintainer_route(self):
        for ident, (_, refs) in read_routes().items():
            if any(ref.startswith("evaluations/") for ref in refs):
                self.assertEqual(ident, "MAINTAIN")

    def test_authored_cases_use_known_disjoint_route_ids(self):
        record = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(record["schema_version"], "1")
        seen = set()
        for case in record["cases"]:
            with self.subTest(case=case["id"]):
                self.assertNotIn(case["id"], seen)
                seen.add(case["id"])
                groups = [set(case[key]) for key in ("primary", "dependencies", "exclude")]
                self.assertTrue(set.union(*groups) <= set(read_routes()))
                self.assertEqual(sum(map(len, groups)), len(set.union(*groups)))
                for key, group in zip(("primary", "dependencies", "exclude"), groups):
                    self.assertEqual(len(case[key]), len(group))
                self.assertTrue(case["prompt"].strip() and case["rationale"].strip())
                self.assertEqual(bool(case["primary"]), case["mode"] != "out_of_scope")
                if case["id"] != "Q13":
                    self.assertNotIn("MAINTAIN", groups[0] | groups[1])
        self.assertEqual(len(seen), 16)


if __name__ == "__main__":
    unittest.main()
