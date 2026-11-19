"""Static contract resource checks, not model reasoning or semantic tests."""
import csv
import unittest
from pathlib import Path

from scripts.build_skill import collect

ROOT = Path(__file__).resolve().parents[1]


class CrossModuleReviewResourceTests(unittest.TestCase):
    def test_resources_in_portable_allowlist(self):
        packaged = collect(ROOT)
        for ref in ("decision-engine/cross-module-review.md",
                    "templates/decision-dependency-review.csv",
                    "examples/cross-module-review/README.md"):
            self.assertIn("seo-engineering/references/library/" + ref, packaged)

    def test_dependency_template_has_distinct_assertion_and_review_fields(self):
        with (ROOT / "templates/decision-dependency-review.csv").open(
                encoding="utf-8", newline="") as handle:
            rows = list(csv.reader(handle))
        self.assertEqual(len(rows), 1)
        fields = rows[0]
        self.assertEqual(len(fields), len(set(fields)))
        self.assertTrue({"prerequisite_decision_id", "dependent_decision_id",
                         "edge_kind", "condition_status", "scope_ref",
                         "required_assertion", "observed_assertion", "evidence_refs",
                         "coverage_and_recency", "comparison_status",
                         "prerequisite_review_status", "dependent_disposition",
                         "next_check", "owner", "reviewer"} <= set(fields))

    def test_conditional_router_reference_not_unconditional_route_row(self):
        router = (ROOT / "skills/seo-engineering/references/router.md").read_text(encoding="utf-8")
        ref = "decision-engine/cross-module-review.md"
        self.assertIn(ref, router)
        self.assertFalse(any(ref in row for row in router.splitlines() if row.startswith("| ")))


if __name__ == "__main__":
    unittest.main()
