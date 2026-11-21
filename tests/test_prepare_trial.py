import copy
import tempfile
import unittest
from pathlib import Path

from scripts.build_skill import build, LIBRARY_DIRS
from scripts.control_benchmark import schedule, fingerprint, blind_packet
from scripts.prepare_trial import stage, initial_ledger, check_artifacts, compare_reviewers, tree_hashes
from scripts.verify_package import digest

class TrialTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.tmp=Path(temp.name)
        self.root=self.tmp/"source"
        def write(name,data="demo"):
            p=self.root/name
            p.parent.mkdir(parents=True,exist_ok=True)
            p.write_text(data,encoding="utf-8")
        for name in LIBRARY_DIRS: write(name+"/demo.md")
        write("evaluations/cases.json",'{"secret":"fictional rubric"}')
        write("skills/seo-engineering/SKILL.md","---\nname: seo-engineering\ndescription: Synthetic skill\n---\n# Skill\n")
        write("skills/seo-engineering/references/router.md")
        write("skills/seo-engineering/references/execution-contract.md")
        for name in ("audit_html.py","check_docs.py","cluster_keywords.py","audit_topic_graph.py",
                     "prioritize_opportunities.py","audit_locale_manifest.py","validate_research.py",
                     "inspect_architecture.py","audit_rendering.py","audit_spa_build.py","audit_next_delivery.py",
                     "audit_crawl_evidence.py","audit_index_evidence.py","audit_migration.py",
                     "audit_metadata.py","audit_performance.py","audit_technical.py",
                     "review_release_gates.py","review_incident.py","README.md"):
            write("scripts/"+name)
        self.archive=self.tmp/"skill.zip";build(self.root,self.archive)
        self.context=self.tmp/"context.txt";self.context.write_text("Common fictional input",encoding="utf-8")
        self.suite={"version":"fixture","cases":[{"id":"A","prompt":"Task","expected":["good"],"disqualifiers":["bad"]}]}
        self.config=dict(model="fictional model",runtime="fixture runtime",inference_settings="fixed",
            tool_config="matched",permission_mode="read-only",skill_commit="a"*40,
            archive_sha256=digest(self.archive.read_bytes()),launch_protocol="fresh sessions",
            review_protocol="blind reviewers",suite_kind="public_regression",repeats=1,
            treatment="complete_toolkit",task_context_sha256=digest(self.context.read_bytes()),
            seed=12,budget="equal",rubric_access_policy="restricted",candidate_variant="rubric_restricted")
        self.ctl=schedule(self.suite,self.config,["A"])

    def stage(self,arm,ctl=None,runtime_kind="codex"):
        c=ctl or self.ctl
        ident=next(s["blind_id"] for s in c["slots"] if s["arm"]==arm)
        target=self.tmp/(arm if runtime_kind=="codex" else arm+"-"+runtime_kind)
        return stage(self.root,self.suite,c,ident,self.archive,self.context,target,
                     runtime_kind=runtime_kind)

    def test_baseline_and_treatment_context_identical(self):
        b,s=self.stage("baseline"),self.stage("skill")
        self.assertEqual(tree_hashes(self.tmp/"baseline"),{"context.txt":b["context_sha256"]})
        self.assertEqual(b["context_sha256"],s["context_sha256"])
        self.assertFalse(any("/evaluations/" in path for path in s["installed_files"]))
        self.assertTrue(any(p.endswith("cases.json") for p in s["omitted_archive_paths"]))
        self.assertEqual(s["runtime_activation"],"not_tested")
        self.assertFalse(s["actual_model_run"])

    def test_cursor_layout_is_explicit_and_rubric_restricted(self):
        rec=self.stage("skill",runtime_kind="cursor")
        files=tree_hashes(self.tmp/"skill-cursor")
        self.assertIn(".cursor/skills/seo-engineering/SKILL.md",files)
        self.assertFalse(any(p.startswith(".agents/skills/") for p in files))
        self.assertFalse(any("/evaluations/" in p for p in files))
        self.assertEqual(rec["installed_skill_root"],".cursor/skills/seo-engineering")
        self.assertEqual(rec["runtime_kind"],"cursor")
        self.assertFalse(rec["actual_model_run"])

    def test_invalid_runtime_layout_does_not_write(self):
        with self.assertRaisesRegex(ValueError,"unsupported pilot runtime"):
            self.stage("skill",runtime_kind="unrecognized")
        self.assertFalse((self.tmp/"skill-unrecognized").exists())

    def test_held_out_unmodified_install(self):
        ctl=schedule(self.suite,self.config|{"suite_kind":"held_out","candidate_variant":"unmodified"},["A"])
        s=self.stage("skill",ctl)
        self.assertTrue(any(p.endswith("evaluations/cases.json") for p in s["installed_files"]))
        self.assertEqual(s["omitted_archive_paths"],[])

    def test_bad_context_and_stale_archive(self):
        self.context.write_text("changed")
        with self.assertRaisesRegex(ValueError,"context digest"): self.stage("skill")
        self.context.write_text("Common fictional input")
        (self.root/"docs/demo.md").write_text("evil")
        with self.assertRaisesRegex(ValueError,"content mismatch"): self.stage("skill")
        self.assertFalse((self.tmp/"skill").exists())

    def test_no_overwrite(self):
        self.stage("baseline")
        with self.assertRaisesRegex(ValueError,"fresh target"): self.stage("baseline")

    def ledger(self):
        ledger=initial_ledger(self.ctl)
        root=self.tmp/"artifacts";root.mkdir()
        for index,row in enumerate(ledger["runs"]):
            ident=row["blind_id"]
            folder=root/ident;folder.mkdir()
            row.update(status="completed",session_ref=f"session-{index}",environment_ref="fixture",failure_reason=None)
            for kind in ("output","trace"):
                raw=("synthetic "+kind+str(index)).encode()
                path=folder/(kind+".txt");path.write_bytes(raw)
                row[kind+"_ref"]=ident+"/"+kind+".txt"
                row[kind+"_sha256"]=digest(raw)
        return ledger,root

    def test_actual_bytes_and_tamper(self):
        ledger,root=self.ledger()
        r=check_artifacts(self.ctl,ledger,root)
        self.assertEqual(len(r["verified_artifacts"]),4)
        self.assertFalse(r["actual_execution_verified"])
        (root/ledger["runs"][0]["output_ref"]).write_text("changed")
        with self.assertRaisesRegex(ValueError,"changed"): check_artifacts(self.ctl,ledger,root)

    def test_reference_escape_and_session_reuse(self):
        ledger,root=self.ledger()
        changed=copy.deepcopy(ledger)
        changed["runs"][0]["output_ref"]="../other.txt"
        with self.assertRaisesRegex(ValueError,"reference"): check_artifacts(self.ctl,changed,root)
        ledger["runs"][1]["session_ref"]=ledger["runs"][0]["session_ref"]
        with self.assertRaisesRegex(ValueError,"session reference"): check_artifacts(self.ctl,ledger,root)

    def test_symlink_artifact_rejected(self):
        ledger,root=self.ledger()
        p=root/ledger["runs"][0]["output_ref"]
        other=root/"external.txt";other.write_bytes(p.read_bytes());p.unlink();p.symlink_to(other)
        with self.assertRaisesRegex(ValueError,"regular file"): check_artifacts(self.ctl,ledger,root)

    def test_initial_ledger_all_not_started(self):
        ledger=initial_ledger(self.ctl)
        root=self.tmp/"artifacts";root.mkdir()
        self.assertEqual(len(ledger["runs"]),2)
        self.assertTrue(all(r["status"]=="not_started" for r in ledger["runs"]))
        self.assertEqual(check_artifacts(self.ctl,ledger,root)["verified_artifacts"],[])

    def reviewers(self):
        l,root=self.ledger()
        packet=blind_packet(self.suite,self.ctl,l)
        def make(name):
            return {"packet_sha256":fingerprint(packet),"records":[
                {"blind_id":r["blind_id"],"reviewer":name,"output_sha256":r["output_sha256"],"trace_sha256":r["trace_sha256"],
                 "expected":[{"criterion":1,"status":"pass","evidence":"synthetic"}],
                 "disqualifiers":[{"criterion":1,"status":"absent","evidence":"synthetic"}]}
                for r in packet["records"]]}
        return packet,make("reviewer-a"),make("reviewer-b")

    def test_review_agreement_and_disagreement(self):
        p,a,b=self.reviewers()
        b["records"][0]["disqualifiers"][0]["status"]="observed"
        r=compare_reviewers(p,a,b)
        self.assertEqual(r["agreement_rate"],0.75)
        self.assertTrue(r["adjudication_required"])
        self.assertFalse(r["calibration_certified"])

    def test_missing_reviewer_and_same_reviewer(self):
        p,a,b=self.reviewers()
        b["records"].pop()
        self.assertTrue(compare_reviewers(p,a,b)["adjudication_required"])
        with self.assertRaisesRegex(ValueError,"same reviewer"): compare_reviewers(p,a,a)
