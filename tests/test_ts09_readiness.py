"""Check historical readiness record and refreshed source inventory structure only."""
import csv
import json
import re
import unittest
from pathlib import Path

from scripts.build_skill import collect
from scripts.check_candidate_checkpoint import validate

ROOT = Path(__file__).resolve().parents[1]


class ReadinessReviewTests(unittest.TestCase):
    def test_exact_held_baseline_record(self):
        record = json.loads((ROOT/"operations/ts09-readiness-checkpoint.json").read_text(encoding="utf-8"))
        result = validate(record)
        self.assertEqual(result["candidate"]["source_commit"], "a931f6fde2ecce1d551a8a1e52134049f77b74ac")
        self.assertEqual(result["recorded_passes"], 5)
        self.assertEqual(len(result["open_mandatory_gates"]), 11)
        self.assertFalse(result["release_approved"])
        self.assertFalse(result["evidence_authenticity_verified"])
        self.assertEqual(record["verified_environment"]["archive_files"], 284)

    def test_refreshed_historical_inventory_and_archive_mapping(self):
        def read(name):
            with (ROOT/"operations"/name).open(encoding="utf-8", newline="") as stream:
                return list(csv.DictReader(stream))
        rows = read("ts09-rights-inventory.csv")
        previous = {r["path"]:r["git_blob_oid"] for r in read("ts05-rights-inventory.csv")}
        self.assertEqual(len(rows), 389)
        current = {r["path"]: r for r in rows}
        self.assertEqual(len(current), len(rows))
        self.assertTrue(set(previous) <= set(current))
        counts = {"added":0,"modified":0,"unchanged":0}
        expected = {}
        for p,r in current.items():
            self.assertRegex(r["git_blob_oid"], r"^[0-9a-f]{40}$")
            state = "added" if p not in previous else ("unchanged" if previous[p]==r["git_blob_oid"] else "modified")
            self.assertEqual(r["change_since_ts05_inventory"], state)
            self.assertEqual(r["rights_status"], "pending_review")
            counts[state] += 1
            if r["expected_archive_path"]:
                self.assertNotIn(r["expected_archive_path"], expected)
                expected[r["expected_archive_path"]] = p
        self.assertEqual(counts, {"added":110,"modified":54,"unchanged":225})
        self.assertEqual(len(expected),284)
        # Check current builder mapping for this baseline's existing resources.
        # Future new files do not invalidate the historical inventory.
        actual = collect(ROOT)
        for target,p in expected.items():
            self.assertEqual(actual[target].relative_to(ROOT).as_posix(), p)
        self.assertFalse(any(p.startswith(("interop/","operations/")) for p in expected.values()))


if __name__ == "__main__":
    unittest.main()
