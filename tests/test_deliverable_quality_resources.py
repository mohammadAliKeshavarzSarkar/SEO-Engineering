"""Static resource and handoff checks, not assessments of generated responses."""
import unittest
from pathlib import Path

from scripts.build_skill import collect

ROOT = Path(__file__).resolve().parents[1]


class DeliverableQualityResourceTests(unittest.TestCase):
    def test_optional_delivery_resources_packaged(self):
        packaged = collect(ROOT)
        for path in ("docs/01-foundations/deliverable-quality.md",
                     "templates/delivery-summary.md",
                     "examples/deliverable-quality/README.md"):
            self.assertIn("seo-engineering/references/library/" + path, packaged)

    def test_summary_retains_independent_state_coverage_and_verification(self):
        template = (ROOT / "templates/delivery-summary.md").read_text(encoding="utf-8")
        for heading in ("## Decision and current state", "## Scope and coverage",
                        "## Findings and recommended actions", "## Actual changes and verification",
                        "## Next decisions and supporting artifacts"):
            self.assertEqual(template.count(heading), 1)
        self.assertIn("pass / fail / blocked / not-run / N/A with rationale", template)
        self.assertIn("known denominator or unknown", template)
        self.assertIn("owner or proposed owner", template)

    def test_delivery_handoff_references_and_hypothetical_examples(self):
        contract = (ROOT / "skills/seo-engineering/references/execution-contract.md").read_text(encoding="utf-8")
        self.assertIn("For complex handoffs consult docs/01-foundations/deliverable-quality.md", contract)
        self.assertIn("optionally templates/delivery-summary.md", contract)
        examples = (ROOT / "examples/deliverable-quality/README.md").read_text(encoding="utf-8")
        self.assertIn("not actual findings", examples)
        self.assertIn("not-run", examples)
        self.assertIn("No claimed traffic gain", examples)


if __name__ == "__main__":
    unittest.main()
