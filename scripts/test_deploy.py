"""Exercise installation against isolated checkouts and simulated Mac home folders."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SOURCE = Path(__file__).resolve().parent.parent


class DeploymentTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="coherent-install-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.repo = self.root / "checkout with space's"
        self.repo.mkdir()
        for name in ("skills", "rules", "adapters", "scripts"):
            shutil.copytree(SOURCE / name, self.repo / name, ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copyfile(SOURCE / "AGENTS.md", self.repo / "AGENTS.md")
        self.target = self.root / "user home"

    def run_deploy(self, *args, status=0):
        result = subprocess.run(
            [sys.executable, str(self.repo / "scripts/deploy.py"), "--target-home", str(self.target), *args],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, status, result.stdout + result.stderr)
        return result

    def test_preview_is_read_only(self):
        self.run_deploy("--dry-run")
        self.assertFalse(self.target.exists())
        self.assertFalse((self.repo / ".generated").exists())

    def test_global_install_and_repeat(self):
        local = self.repo / ".agents/skills"
        local.parent.mkdir()
        local.symlink_to("../skills")
        self.run_deploy()
        self.run_deploy("--check")
        self.assertFalse(local.is_symlink())
        for root in (".agents/skills", ".gemini/config/skills"):
            self.assertEqual((self.target / root).resolve(), self.repo / "skills")
            self.assertEqual(len(list((self.target / root).glob("*/SKILL.md"))), 16)
        instructions = self.target / ".codex/AGENTS.md"
        text = instructions.read_text()
        for rule in sorted((self.repo / "rules").glob("*.md")):
            self.assertIn(rule.read_text().split("---", 2)[2].strip(), text)
        before = (instructions.lstat().st_ino, instructions.stat().st_mtime_ns)
        self.run_deploy()
        self.assertEqual(before, (instructions.lstat().st_ino, instructions.stat().st_mtime_ns))

    def test_glob_triggered_rule_is_conditionally_wrapped(self):
        glob_rule = self.repo / "rules/99-test-glob.md"
        glob_rule.write_text(
            '---\ntrigger: glob\nglobs: "*.py"\ndescription: "Python policy."\n---\n# Python Policy\n\n- Scope\n'
        )
        self.run_deploy()
        text = (self.target / ".codex/AGENTS.md").read_text()
        self.assertIn("Apply the following policy only when working on files matching `*.py`.", text)
        self.assertIn("<!-- END CONDITIONAL POLICY -->", text)

    def test_conflict_aborts_before_writes_and_backup_preserves_content(self):
        conflict = self.target / ".gemini/config/hooks.json"
        conflict.parent.mkdir(parents=True)
        conflict.write_text('{"user-owned": true}\n')
        self.run_deploy(status=1)
        self.assertFalse((self.target / ".codex").exists())
        self.assertFalse((self.repo / ".generated").exists())
        self.run_deploy("--backup-conflicts")
        backup = list((self.target / ".local/state/coherent-output/backups").glob("*/*hooks.json"))
        self.assertEqual(len(backup), 1)
        self.assertEqual(backup[0].read_text(), '{"user-owned": true}\n')
        manifest = json.loads((backup[0].parent / "manifest.json").read_text())
        self.assertEqual(manifest, [{"original": str(conflict), "backup": str(backup[0])}])
        self.run_deploy("--check")

    def test_generated_content_drift_is_detected(self):
        self.run_deploy()
        with (self.repo / "rules/01-autonomous-workflow.md").open("a") as stream:
            stream.write("\nA new shared instruction.\n")
        self.run_deploy("--check", status=1)
        self.run_deploy()
        self.run_deploy("--check")
        self.assertIn("A new shared instruction.", (self.target / ".codex/AGENTS.md").read_text())

    def test_only_selected_tool_is_installed(self):
        self.run_deploy("--tool", "codex")
        self.run_deploy("--tool", "codex", "--check")
        self.assertFalse((self.target / ".gemini").exists())
        self.assertFalse((self.repo / ".generated/antigravity").exists())

    def test_existing_mapping_migrates_even_with_missing_old_hook_source(self):
        codex = self.target / ".codex/AGENTS.md"
        hooks = self.target / ".gemini/config/hooks.json"
        alias = self.root / "checkout alias"
        alias.symlink_to(self.repo)
        for destination, source in ((codex, "AGENTS.md"), (hooks, "hooks/hooks.json")):
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.symlink_to(alias / source)
        self.run_deploy()
        self.run_deploy("--check")

    def test_hook_commands_handle_spaces_and_keep_antigravity_contract(self):
        self.run_deploy()
        config = json.loads((self.target / ".gemini/config/hooks.json").read_text())
        command = config["destructive-command-safety-gate"]["PreToolUse"][0]["hooks"][0]["command"]
        for sample, expected in (("pwd", "allow"), ("git reset --hard", "force_ask"), ("rm -rf /example", "force_ask")):
            # Command samples are stdin data for the gate; they are never executed.
            result = subprocess.run(
                ["/bin/bash", "-c", command],
                input=json.dumps({"toolCall": {"args": {"CommandLine": sample}}}),
                text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["decision"], expected)

    def test_prettier_hook_handles_quoted_paths_and_keeps_antigravity_contract(self):
        self.run_deploy()
        config = json.loads((self.target / ".gemini/config/hooks.json").read_text())
        command = config["prettier-auto-format"]["PostToolUse"][0]["hooks"][0]["command"]
        sample_file = self.target / "sample.md"
        sample_file.write_text("#  Header\n\n-  item\n")
        for target in (str(sample_file), f'"{sample_file}"'):
            result = subprocess.run(
                ["/bin/bash", "-c", command],
                input=json.dumps({"toolCall": {"name": "write_to_file", "args": {"TargetFile": target}}}),
                text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout), {})


if __name__ == "__main__":
    unittest.main()

