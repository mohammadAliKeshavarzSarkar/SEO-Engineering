import tempfile
import unittest
from pathlib import Path
import json
from scripts.start_public_pilot import prepare, separate
from scripts.build_skill import LIBRARY_DIRS

class StartPilotTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.base=Path(tmp.name)
        self.root=self.base/"checkout"
        def write(name,text):
            p=self.root/name
            p.parent.mkdir(parents=True,exist_ok=True)
            p.write_text(text,encoding="utf-8")
        for d in LIBRARY_DIRS: write(d+"/demo.md","demo")
        ids=[f"C{i}" for i in range(16)]
        write("evaluations/cases.json",json.dumps({"version":"test","cases":[
            {"id":i,"prompt":"Synthetic "+i,"expected":["good"],"disqualifiers":["bad"]}
            for i in ids]}))
        write("evaluations/public-pilot.json",json.dumps({"case_ids":ids}))
        write("skills/seo-engineering/SKILL.md","---\nname: seo-engineering\ndescription: Test skill\n---\n")
        write("skills/seo-engineering/references/router.md","router")
        write("skills/seo-engineering/references/execution-contract.md","contract")
        for name in ("audit_html.py","check_docs.py","cluster_keywords.py","audit_topic_graph.py","prioritize_opportunities.py",
            "audit_locale_manifest.py","validate_research.py","inspect_architecture.py","audit_rendering.py",
            "audit_spa_build.py","audit_next_delivery.py","audit_crawl_evidence.py","audit_index_evidence.py",
            "audit_migration.py","audit_metadata.py","audit_performance.py","audit_technical.py",
            "review_release_gates.py","review_incident.py","README.md"):
            write("scripts/"+name,"demo")
        self.cfg=dict(model="fictional",runtime="fictional",inference_settings="fixed",
            tool_config="none",permission_mode="read-only",launch_protocol="fresh",
            review_protocol="blind",suite_kind="public_regression",repeats=1,treatment="complete_toolkit",
            seed=12,budget="equal",rubric_access_policy="restricted",candidate_variant="rubric_restricted")

    def test_first_pair_only_and_no_rubric(self):
        op,work=self.base/"operator",self.base/"work"
        r=prepare(self.root,"a"*40,self.cfg,op,work)
        self.assertEqual((r["planned_slots"],r["staged_slots"],r["actual_agent_runs"]),(32,2,0))
        self.assertEqual(len(list(work.iterdir())),2)
        a,b=r["first_pair_in_launch_order"]
        self.assertEqual(a["case_id"],b["case_id"])
        self.assertNotEqual(a["arm"],b["arm"])
        self.assertEqual(Path(a["prompt_file"]).read_bytes(),Path(b["prompt_file"]).read_bytes())
        for s in (a,b):
            folder=Path(s["workspace"])
            self.assertFalse(any(folder.rglob("cases.json")))
            self.assertFalse((folder/"launch.json").exists())
        self.assertTrue(all(x["status"]=="not_started" for x in json.loads((op/"ledger.json").read_bytes())["runs"]))
        self.assertEqual(r["runtime_isolation"],"not_verified")
        with self.assertRaisesRegex(ValueError,"fresh"): prepare(self.root,"a"*40,self.cfg,op,work)

    def test_invalid_config_and_nested_paths(self):
        op,work=self.base/"operator",self.base/"work"
        with self.assertRaisesRegex(ValueError,"derived"):
            prepare(self.root,"a"*40,self.cfg|{"archive_sha256":"b"*64},op,work)
        with self.assertRaisesRegex(ValueError,"non-nested"):
            separate((self.root,op,op/"nested"))
        with self.assertRaisesRegex(ValueError,"reviewed config"):
            prepare(self.root,"a"*40,self.cfg|{"model":"REPLACE exact"},op,work)
        self.assertFalse(op.exists())
