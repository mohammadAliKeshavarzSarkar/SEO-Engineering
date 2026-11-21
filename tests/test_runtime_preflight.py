"""Local installation checks without executing a coding agent."""
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from scripts.build_skill import ROOT, build
from scripts.preflight_runtime import inspect


class RuntimePreflightTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)
        self.archive = self.home / "snapshot.zip"
        build(ROOT, self.archive)

    def install(self, runtime):
        project = self.home / ("project " + runtime)
        target = project / (".agents" if runtime == "codex" else ".cursor") / "skills"
        target.mkdir(parents=True)
        with ZipFile(self.archive) as z:
            z.extractall(target)
        return target / "seo-engineering"

    def test_codex_path_and_cli_detection_are_not_activation(self):
        installed = self.install("codex")
        rec = inspect(ROOT, self.archive, installed, "codex",
                      which=lambda name: "/fictional/codex" if name == "codex" else None)
        self.assertEqual(rec["status"], "ready_for_operator_activation_probe")
        self.assertEqual(rec["command_names_on_path"], ["codex"])
        self.assertFalse(rec["skill_discovery_observed"])
        self.assertFalse(rec["read_isolation_verified"])
        self.assertFalse(rec["release_approved"])

    def test_cursor_path_and_absent_cli_remains_blocked(self):
        installed = self.install("cursor")
        rec = inspect(ROOT, self.archive, installed, "cursor", which=lambda name: None)
        self.assertEqual(rec["status"], "blocked_cli_not_found")
        self.assertTrue(rec["exact_installed_bytes_checked"])
        self.assertFalse(rec["model_inference_performed"])

    def test_wrong_placement_or_mutated_installation_rejected(self):
        installed = self.install("codex")
        with self.assertRaisesRegex(ValueError, "selected project skill path"):
            inspect(ROOT, self.archive, installed, "cursor", which=lambda n: n)
        path = installed / "SKILL.md"
        path.write_bytes(path.read_bytes()+b"\nmodified\n")
        with self.assertRaisesRegex(ValueError, "installed content mismatch"):
            inspect(ROOT, self.archive, installed, "codex", which=lambda n: n)

    def test_parent_checkout_installation_rejected(self):
        # A path under the source checkout is not an isolated target.
        with self.assertRaises(ValueError):
            inspect(ROOT, self.archive, ROOT / ".agents/skills/seo-engineering",
                    "codex", which=lambda n: n)


if __name__ == "__main__":
    unittest.main()
