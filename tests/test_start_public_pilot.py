import tempfile
import unittest
from pathlib import Path
import json
from scripts.start_public_pilot import prepare, separate
from scripts.check_pilot_staging import inspect as inspect_pair
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

    def test_cursor_pair_has_correct_layout_and_identical_prompts(self):
        op,work=self.base/"cursor-operator",self.base/"cursor-work"
        cfg=self.cfg|{"runtime":"Cursor CLI 0-fixture"}
        result=prepare(self.root,"a"*40,cfg,op,work,runtime_kind="cursor")
        self.assertEqual(result["runtime_kind"],"cursor")
        self.assertFalse(result["runtime_activation_observed"])
        pair=result["first_pair_in_launch_order"]
        self.assertEqual(pair[0]["case_id"],pair[1]["case_id"])
        self.assertEqual(Path(pair[0]["prompt_file"]).read_bytes(),
                         Path(pair[1]["prompt_file"]).read_bytes())
        self.assertEqual({s["arm"] for s in pair},{"baseline","skill"})
        for s in pair:
            folder=Path(s["workspace"])
            if s["arm"]=="skill":
                self.assertTrue((folder/".cursor/skills/seo-engineering/SKILL.md").is_file())
                self.assertFalse((folder/".agents").exists())
                self.assertFalse(any(folder.rglob("cases.json")))
            else:
                self.assertEqual(sorted(p.relative_to(folder).as_posix() for p in folder.rglob("*")
                                        if p.is_file()),["context.txt"])

    def test_declared_runtime_mismatch_rejected_before_creating_roots(self):
        op,work=self.base/"operator",self.base/"work"
        cfg=self.cfg|{"runtime":"Cursor CLI 0-fixture"}
        with self.assertRaisesRegex(ValueError,"differs from installation layout"):
            prepare(self.root,"a"*40,cfg,op,work,runtime_kind="codex")
        self.assertFalse(op.exists())
        self.assertFalse(work.exists())

    def test_first_pair_pre_run_integrity_both_runtimes(self):
        for kind in ("codex","cursor"):
            with self.subTest(kind=kind):
                op,work=self.base/(kind+"-operator"),self.base/(kind+"-work")
                cfg=self.cfg|{"runtime":kind.title()+" CLI fixture"}
                prepare(self.root,"a"*40,cfg,op,work,runtime_kind=kind)
                result=inspect_pair(self.root,op,work)
                self.assertEqual(result["runtime_kind"],kind)
                self.assertEqual(result["planned_slots"],32)
                self.assertEqual(len(result["verified_unstarted_pair"]),2)
                self.assertTrue(result["matched_task_and_prompt"])
                self.assertTrue(result["stage_bytes_matched_to_source_archive"])
                self.assertFalse(result["filesystem_read_isolation_verified"])
                self.assertFalse(result["runtime_discovery_verified"])
                self.assertFalse(result["release_approved"])

    def test_first_pair_tampered_skill_or_prompt_rejected(self):
        op,work=self.base/"operator",self.base/"work"
        p=prepare(self.root,"a"*40,self.cfg,op,work)
        skill=next(s for s in p["first_pair_in_launch_order"] if s["arm"]=="skill")
        doc=Path(skill["workspace"])/".agents/skills/seo-engineering/SKILL.md"
        doc.write_text("changed",encoding="utf-8")
        with self.assertRaisesRegex(ValueError,"staged files changed"):
            inspect_pair(self.root,op,work)
        doc.write_text("---\\nname: seo-engineering\\ndescription: Test skill\\n---\\n",encoding="utf-8")
        prompt=Path(skill["prompt_file"])
        prompt.write_text("different prompt",encoding="utf-8")
        with self.assertRaisesRegex(ValueError,"staged prompt changed"):
            inspect_pair(self.root,op,work)

    def test_first_pair_changed_ledger_or_control_rejected(self):
        op,work=self.base/"operator",self.base/"work"
        prepare(self.root,"a"*40,self.cfg,op,work)
        ledger=op/"ledger.json"
        record=json.loads(ledger.read_text(encoding="utf-8"))
        record["runs"][0]["status"]="timeout"
        ledger.write_text(json.dumps(record),encoding="utf-8")
        with self.assertRaises(ValueError):
            inspect_pair(self.root,op,work)
        # A different frozen control also fails before the modified ledger is inspected.
        control=op/"control.json"
        packet=json.loads(control.read_text(encoding="utf-8"))
        packet["slots"][0]["arm"]="skill" if packet["slots"][0]["arm"]=="baseline" else "baseline"
        control.write_text(json.dumps(packet),encoding="utf-8")
        with self.assertRaisesRegex(ValueError,"control differs"):
            inspect_pair(self.root,op,work)

    def test_invalid_config_and_nested_paths(self):
        op,work=self.base/"operator",self.base/"work"
        with self.assertRaisesRegex(ValueError,"derived"):
            prepare(self.root,"a"*40,self.cfg|{"archive_sha256":"b"*64},op,work)
        with self.assertRaisesRegex(ValueError,"non-nested"):
            separate((self.root,op,op/"nested"))
        with self.assertRaisesRegex(ValueError,"reviewed config"):
            prepare(self.root,"a"*40,self.cfg|{"model":"REPLACE exact"},op,work)
        self.assertFalse(op.exists())
