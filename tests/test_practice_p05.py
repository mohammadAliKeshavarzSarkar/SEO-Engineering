"""End-to-end local practice CLI and safety-boundary regressions."""
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.build_skill import collect

ROOT=Path(__file__).resolve().parents[1]
LAB=ROOT/"examples/practice-projects/p05-capstone"
spec=importlib.util.spec_from_file_location("p05_lab",LAB/"run_lab.py")
lab=importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)


class PracticeP05Tests(unittest.TestCase):
    def cli(self,out):
        return subprocess.run([sys.executable,"-B",str(LAB/"run_lab.py"),"--out",str(out)],
                              cwd=ROOT,capture_output=True,text=True,timeout=45)

    def test_actual_capstone_cli_receipt(self):
        original=lab.hashes(lab.P03/"p03-a/artifacts")
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/"receipt.json"
            proc=self.cli(out)
            self.assertEqual(proc.returncode,0,proc.stdout+proc.stderr)
            r=json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(set(r["changed_files"]),lab.PATCH_FILES)
        self.assertEqual(r["initial_hashes"],original)
        self.assertEqual(lab.hashes(lab.P03/"p03-a/artifacts"),original)
        self.assertEqual({k for k,v in original.items() if v!=r["candidate_hashes"][k]},lab.PATCH_FILES)
        self.assertTrue(r["source_unchanged"] and r["disposable_copy_removed"])
        reports=r["reports"]
        self.assertEqual(reports["html-before"]["exit_code"],1)
        self.assertEqual(reports["html-after"]["exit_code"],0)
        self.assertEqual(len(reports["locale-after"]["report"]["findings"]),2)
        self.assertEqual(reports["handoff"]["report"]["provisional"],["U3","U4"])
        after={x["id"]:x for x in reports["priority-after"]["report"]["rows"]}
        self.assertEqual(after["review-guide-copy"]["lane"],"growth")
        self.assertEqual(after["actual-browser-qa"]["lane"],"review")
        self.assertEqual(after["unsupported-hours"]["lane"],"excluded")
        self.assertTrue(all(x["authorization_required"] for x in after.values()))
        gate=reports["gate"]["report"]
        local=next(x for x in gate["gates"] if x["id"]=="local-html")
        self.assertEqual(local["state"],"pass")
        digest=hashlib.sha256(json.dumps(reports["html-after"],sort_keys=True).encode()).hexdigest()
        self.assertEqual(local["evidence"]["ref"],"receipt:html-after:sha256:"+digest)
        self.assertEqual(gate["disposition"],"hold")
        self.assertEqual(set(gate["blockers"]),{"browser-locale","access","measurement"})
        self.assertFalse(gate["evidence_independently_verified"])
        for key in ("actual_external_verification","deployment_authorized","search_or_business_growth_established"):
            self.assertFalse(r[key])

    def test_failed_anchor_prevents_all_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/"artifacts"
            shutil.copytree(lab.P03/"p03-a/artifacts",target)
            path=target/"en/service/index.html"
            path.write_bytes(path.read_bytes().replace(b'hreflang="en"',b'hreflang="xx"'))
            before=lab.hashes(target)
            with self.assertRaisesRegex(ValueError,"patch precondition"):
                lab.apply(target,lab.load(lab.P03/"registry.json"))
            self.assertEqual(lab.hashes(target),before)

    def test_output_existing_rejected_without_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/"receipt.json"
            out.write_bytes(b"preserve")
            proc=self.cli(out)
            self.assertEqual(proc.returncode,1)
            self.assertEqual(out.read_bytes(),b"preserve")

    def test_resources_packaged(self):
        packaged=collect(ROOT)
        for name in ("README.md","decision-plan.md","backlog.json","run_lab.py"):
            self.assertIn("seo-engineering/references/library/examples/practice-projects/p05-capstone/"+name,packaged)


if __name__=="__main__":
    unittest.main()
