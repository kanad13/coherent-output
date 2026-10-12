"""Exercise installation against isolated checkouts and simulated Mac homes.

Generated commands must work from the installed artifacts, not only the source
scripts. Isolation makes backup and migration tests safe for existing app state.
"""

import json
import os
from pathlib import Path
import shutil
import shlex
import subprocess
import sys
import tempfile
import unittest


SOURCE = Path(__file__).resolve().parent.parent


class DeploymentTests(unittest.TestCase):
    """Verify installation ownership and observable host-command effects."""

    def setUp(self):
        """Keep installation writes and device-owned state outside the real home."""
        self.temporary = tempfile.TemporaryDirectory(prefix="coherent-install-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.repo = self.root / "checkout with space's"
        self.repo.mkdir()
        for name in ("skills", "rules", "adapters", "scripts", "instructions", "docs", ".githooks"):
            shutil.copytree(SOURCE / name, self.repo / name, ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copyfile(SOURCE / ".prettierrc", self.repo / ".prettierrc")
        shutil.copyfile(SOURCE / ".prettierignore", self.repo / ".prettierignore")
        (self.repo / "node_modules").symlink_to(SOURCE / "node_modules", target_is_directory=True)
        self.target = self.root / "user home"

    def run_deploy(self, *args, status=0):
        """Require the installer's reported result to match its expected outcome.

        Args:
            *args: Additional installer CLI arguments.
            status: Expected process exit status.

        Returns:
            The completed installer process for further result assertions.
        """
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
            self.assertEqual(
                len(list((self.target / root).glob("*/SKILL.md"))),
                len(list((self.repo / "skills").glob("*/SKILL.md"))),
            )
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
        with (self.repo / "instructions/global.md").open("a") as stream:
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

    def test_antigravity_only_install_accepts_native_manual_and_model_rules(self):
        """Keep Codex composition constraints out of Antigravity-only deployment."""
        rule = self.repo / "rules/99-native-policy.md"
        for trigger in ("manual", "model_decision"):
            with self.subTest(trigger=trigger):
                rule.write_text(f"---\ntrigger: {trigger}\ndescription: Native Antigravity policy.\n---\n# Native Policy\n")
                self.run_deploy("--tool", "antigravity")
                self.run_deploy("--tool", "antigravity", "--check")
                self.assertFalse((self.repo / ".generated/codex").exists())
                self.assertEqual((self.target / ".gemini/config/rules/99-native-policy.md").read_text(), rule.read_text())
                self.run_deploy("--tool", "codex", "--dry-run", status=1)

    def test_codex_only_install_does_not_parse_antigravity_templates(self):
        """Prevent unrelated host configuration from blocking Codex deployment."""
        (self.repo / "adapters/antigravity/hooks/hooks.template.json").write_text("not-json")
        self.run_deploy("--tool", "codex")
        self.run_deploy("--tool", "codex", "--check")
        self.assertFalse((self.target / ".gemini").exists())

    @unittest.skipUnless(sys.platform == "darwin", "Mac GUI runtime discovery contract")
    def test_codex_installed_checker_starts_without_python_on_gui_path(self):
        """Exercise the interpreter bootstrap before the checker's PATH setup."""
        self.run_deploy("--tool", "codex")
        config = json.loads((self.target / ".codex/hooks.json").read_text())
        command = config["hooks"]["PostToolUse"][0]["hooks"][0]["command"]
        gui_bin = self.root / "gui-bin"
        gui_bin.mkdir()
        sample = self.target / "sample.md"
        sample.write_text("#  Header\n\n-  item\n")
        result = subprocess.run(
            ["/bin/bash", "-c", command],
            input=json.dumps({"tool_name": "Write", "tool_input": {"file_path": str(sample)}}),
            cwd=self.root, env={**os.environ, "PATH": str(gui_bin)},
            capture_output=True, text=True, timeout=100,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {})
        self.assertEqual(sample.read_text(), "# Header\n\n- item\n")

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
            self.assertEqual(sample_file.read_text(), "# Header\n\n- item\n")

    @unittest.skipUnless(sys.platform == "darwin", "Mac GUI runtime discovery contract")
    def test_antigravity_only_install_runs_all_generated_hooks_without_shell_profile(self):
        """Exercise installed commands without inheriting terminal runtime paths."""
        self.run_deploy("--tool", "antigravity")
        self.run_deploy("--tool", "antigravity", "--check")
        self.assertFalse((self.target / ".codex").exists())
        self.assertEqual((self.target / ".gemini/config/skills").resolve(), self.repo / "skills")
        self.assertTrue((self.target / ".gemini/config/skills/mermaid-architect/scripts/verify-markdown.py").is_file())
        config = json.loads((self.target / ".gemini/config/hooks.json").read_text())
        gui_bin = self.root / "gui-bin"
        gui_bin.mkdir()
        (gui_bin / "dirname").symlink_to(shutil.which("dirname"))
        environment = {**os.environ, "PATH": str(gui_bin)}

        def invoke(name, event, payload):
            """Exercise the rendered command through the native shell boundary."""
            command = config[name][event][0]["hooks"][0]["command"]
            self.assertTrue(config[name]["enabled"])
            return subprocess.run(
                ["/bin/bash", "-c", command], input=json.dumps(payload),
                cwd=self.root, env=environment, capture_output=True, text=True, timeout=100,
            )

        gate = invoke("destructive-command-safety-gate", "PreToolUse", {"toolCall": {"args": {"CommandLine": "git reset --hard"}}})
        self.assertEqual(gate.returncode, 0, gate.stderr)
        self.assertEqual(json.loads(gate.stdout)["decision"], "force_ask")
        sample = self.target / "document with space's.md"
        sample.write_text("#  Header\n\n-  item\n")
        payload = {"toolCall": {"name": "write_to_file", "args": {"TargetFile": str(sample)}}}
        formatted = invoke("prettier-auto-format", "PostToolUse", payload)
        self.assertEqual(formatted.returncode, 0, formatted.stderr)
        self.assertEqual(json.loads(formatted.stdout), {})
        self.assertEqual(sample.read_text(), "# Header\n\n- item\n")
        for diagram, expected in (("flowchart LR\n A-->B", 0), ("flowchart LR\n A-->", 2)):
            with self.subTest(diagram=diagram):
                sample.write_text("```mermaid\n" + diagram + "\n```\n")
                compiled = invoke("mermaid-syntax-validator", "PostToolUse", payload)
                self.assertEqual(compiled.returncode, expected, compiled.stderr)
                self.assertEqual(json.loads(compiled.stdout), {})
                if expected:
                    self.assertIn("failed compilation", compiled.stderr)

    def test_codex_hook_adoption_preserves_other_handlers_and_settings(self):
        destination = self.target / ".codex/hooks.json"
        destination.parent.mkdir(parents=True)
        unrelated = {"type": "command", "command": "echo personal-hook"}
        owned = {"type": "command", "command": "python3 " + shlex.quote(str(self.repo / "adapters/shared/document-check.py")) + " --host codex"}
        original = {"custom": True, "hooks": {"Stop": [{"hooks": [unrelated]}], "PostToolUse": [{"matcher": ".*", "hooks": [owned, unrelated]}]}}
        destination.write_text(json.dumps(original))
        self.run_deploy(status=1)
        self.assertFalse((self.repo / ".generated").exists())
        self.run_deploy("--backup-conflicts")
        installed = json.loads(destination.read_text())
        self.assertTrue(installed["custom"])
        self.assertEqual(installed["hooks"]["Stop"], original["hooks"]["Stop"])
        self.assertEqual(installed["hooks"]["PostToolUse"][0]["hooks"], [unrelated])
        self.assertEqual(len(installed["hooks"]["PostToolUse"]), 2)
        before = destination.read_text()
        self.run_deploy()
        self.assertEqual(destination.read_text(), before)
        self.run_deploy("--check")

    def test_invalid_codex_hook_schema_aborts_before_writing(self):
        destination = self.target / ".codex/hooks.json"
        destination.parent.mkdir(parents=True)
        destination.write_text('{"hooks": {"PostToolUse": "invalid"}}')
        self.run_deploy("--backup-conflicts", status=1)
        self.assertFalse((self.repo / ".generated").exists())
        self.assertFalse((self.target / ".agents").exists())

    def test_multiple_codex_homes_keep_unrelated_hook_state_isolated(self):
        first = self.target / ".codex/hooks.json"
        first.parent.mkdir(parents=True)
        personal = {"matcher": ".*", "hooks": [{"type": "command", "command": "echo personal"}]}
        first.write_text(json.dumps({"hooks": {"Stop": [personal]}}))
        self.run_deploy("--tool", "codex", "--backup-conflicts")
        before = first.read_text()
        second_home = self.root / "second home"
        self.run_deploy("--tool", "codex", "--target-home", str(second_home))
        second = second_home / ".codex/hooks.json"
        self.assertNotEqual(first.resolve(), second.resolve())
        self.assertEqual(first.read_text(), before)
        self.assertNotIn("Stop", json.loads(second.read_text())["hooks"])
        self.run_deploy("--tool", "codex", "--check")

    def test_claude_install_links_skills_instructions_and_merges_settings(self):
        """Claude Code owns settings.json, so unrelated keys and hooks must survive the merge."""
        settings = self.target / ".claude/settings.json"
        settings.parent.mkdir(parents=True)
        unrelated = {"type": "command", "command": "echo personal"}
        original = {"switchModelsOnFlag": False, "hooks": {"PostToolUse": [{"matcher": "Bash", "hooks": [unrelated]}]}}
        settings.write_text(json.dumps(original))
        settings.chmod(0o600)
        self.run_deploy("--tool", "claude")
        self.run_deploy("--tool", "claude", "--check")
        self.assertEqual((self.target / ".claude/skills").resolve(), self.repo / "skills")
        self.assertEqual((self.target / ".claude/CLAUDE.md").read_text(), (self.repo / "instructions/global.md").read_text().rstrip() + "\n")
        installed = json.loads(settings.read_text())
        self.assertIs(installed["switchModelsOnFlag"], False)
        self.assertEqual(installed["hooks"]["PostToolUse"][0], original["hooks"]["PostToolUse"][0])
        self.assertEqual(installed["hooks"]["PostToolUse"][1]["matcher"], "Write|Edit|MultiEdit")
        self.assertEqual(installed["hooks"]["PreToolUse"][0]["matcher"], "Bash")
        self.assertEqual(settings.stat().st_mode & 0o777, 0o600)
        self.assertEqual(len(list((self.target / ".local/state/coherent-output/backups").glob("*/merged-settings.json"))), 1)
        before = settings.read_text()
        self.run_deploy("--tool", "claude")
        self.assertEqual(settings.read_text(), before)
        self.assertFalse((self.target / ".codex").exists())
        self.assertFalse((self.target / ".gemini").exists())

    def test_claude_installed_hook_formats_edits_and_reports_failure(self):
        self.run_deploy("--tool", "claude")
        command = json.loads((self.target / ".claude/settings.json").read_text())["hooks"]["PostToolUse"][0]["hooks"][0]["command"]
        sample = self.target / "sample.md"
        sample.write_text("#  Header\n\n-  item\n")
        result = subprocess.run(
            ["/bin/bash", "-c", command],
            input=json.dumps({"tool_name": "Edit", "tool_input": {"file_path": str(sample)}}),
            cwd=self.root, capture_output=True, text=True, timeout=100,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(sample.read_text(), "# Header\n\n- item\n")
        sample.write_text("```mermaid\nflowchart LR\n A-->\n```\n")
        result = subprocess.run(
            ["/bin/bash", "-c", command],
            input=json.dumps({"tool_name": "Write", "tool_input": {"file_path": str(sample)}}),
            cwd=self.root, capture_output=True, text=True, timeout=100,
        )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("failed compilation", result.stderr)

    def test_claude_installed_safety_gate_asks_before_destructive_commands(self):
        self.run_deploy("--tool", "claude")
        command = json.loads((self.target / ".claude/settings.json").read_text())["hooks"]["PreToolUse"][0]["hooks"][0]["command"]
        for sample, asks in (("git reset --hard", True), ("pwd", False)):
            result = subprocess.run(
                ["/bin/bash", "-c", command],
                input=json.dumps({"tool_name": "Bash", "tool_input": {"command": sample}}),
                cwd=self.root, capture_output=True, text=True, timeout=30,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(bool(result.stdout), asks)

    def test_claude_merge_keeps_unrelated_handlers_in_every_event_once(self):
        settings = self.target / ".claude/settings.json"
        settings.parent.mkdir(parents=True)
        personal = {"type": "command", "command": "echo personal"}
        original = {"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [personal]}], "Stop": [{"hooks": [personal]}]}}
        settings.write_text(json.dumps(original))
        for _ in range(2):
            self.run_deploy("--tool", "claude")
        installed = json.loads(settings.read_text())["hooks"]
        self.assertEqual(installed["Stop"], original["hooks"]["Stop"])
        pre = [handler["command"] for group in installed["PreToolUse"] for handler in group["hooks"]]
        self.assertEqual(pre.count("echo personal"), 1)
        self.assertEqual(len([command for command in pre if "safety-gate.py" in command]), 1)

    def test_real_install_points_the_clone_at_the_commit_gate(self):
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        self.run_deploy("--tool", "claude")
        configured = subprocess.run(["git", "-C", str(self.repo), "config", "core.hooksPath"], capture_output=True, text=True)
        self.assertEqual(configured.stdout.strip(), ".githooks")

    def test_commit_gate_refuses_misformatted_files_and_accepts_clean_ones(self):
        gate = self.repo / ".githooks/pre-commit"
        clean = subprocess.run(["bash", str(gate)], capture_output=True, text=True, cwd=self.repo, timeout=100)
        self.assertEqual(clean.returncode, 0, clean.stdout + clean.stderr)
        (self.repo / "notes.md").write_text("#  Header\n\n-  item\n")
        dirty = subprocess.run(["bash", str(gate)], capture_output=True, text=True, cwd=self.repo, timeout=100)
        self.assertEqual(dirty.returncode, 1)
        self.assertIn("formatting differs", dirty.stderr)

    def test_invalid_claude_settings_abort_before_writing(self):
        settings = self.target / ".claude/settings.json"
        settings.parent.mkdir(parents=True)
        settings.write_text("{not json")
        self.run_deploy("--tool", "claude", status=1)
        self.assertFalse((self.repo / ".generated").exists())
        self.assertEqual(settings.read_text(), "{not json")

    def test_skill_identity_and_description_limits_are_enforced(self):
        skill = self.repo / "skills/worth-the-squeeze/SKILL.md"
        original = skill.read_text()
        for name in ("WRONG", "-wrong", "wrong--name", "x" * 65, "valid-but-mismatched"):
            with self.subTest(name=name):
                skill.write_text(original.replace("name: worth-the-squeeze", "name: " + name))
                self.run_deploy("--dry-run", status=1)
        skill.write_text("---\nname: worth-the-squeeze\ndescription: " + "x" * 1025 + "\n---\nBody\n")
        self.run_deploy("--dry-run", status=1)


    def edit_graph_cell(self, skill, column, value):
        """Rewrite one cell of the call-graph table in the isolated checkout.

        Args:
            skill: Skill whose row changes.
            column: Header text of the cell to replace, such as ``Optional calls``.
            value: New cell text.
        """
        document = self.repo / "docs/skills.md"
        lines = document.read_text().splitlines()
        header = next(line for line in lines if "Optional calls" in line)
        names = [cell.strip() for cell in header.strip().strip("|").split("|")]
        for number, line in enumerate(lines):
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if line.startswith("| [" + skill + "]") and len(cells) == len(names):
                cells[names.index(column)] = value
                lines[number] = "| " + " | ".join(cells) + " |"
        document.write_text("\n".join(lines) + "\n")

    def assert_graph_refused(self, expected):
        """Require a dry run to fail with the named graph problem."""
        result = self.run_deploy("--dry-run", status=1)
        self.assertIn("call graph is inconsistent", result.stderr)
        self.assertIn(expected, result.stderr)

    def test_graph_rejects_unknown_callee(self):
        self.edit_graph_cell("grill-me", "Optional calls", "web-research, ghost-skill")
        self.assert_graph_refused("unknown skill 'ghost-skill'")

    def test_graph_rejects_cycle(self):
        self.edit_graph_cell("web-research", "Optional calls", "claim-validator")
        self.assert_graph_refused("call cycle: claim-validator -> web-research -> claim-validator")

    def test_graph_rejects_called_workflow(self):
        self.edit_graph_cell("claim-validator", "Optional calls", "web-research, grill-me")
        self.assert_graph_refused("calls workflow 'grill-me'")

    def test_graph_rejects_undeclared_body_reference(self):
        skill = self.repo / "skills/web-research/SKILL.md"
        skill.write_text(skill.read_text() + "\nAsk commit-scribe to save the findings.\n")
        self.assert_graph_refused("text names 'commit-scribe' but its table row does not list it")

    def test_graph_rejects_stale_table_entry(self):
        self.edit_graph_cell("commit-scribe", "Optional calls", "web-research")
        self.assert_graph_refused("table lists 'web-research' but the text never names it")

    def test_graph_requires_callee_mode_line_in_calling_lens(self):
        skill = self.repo / "skills/claim-validator/SKILL.md"
        skill.write_text(skill.read_text().replace("Callee mode", "Nested use"))
        self.assert_graph_refused("has no 'Callee mode' line")

    def test_graph_rejects_skill_missing_from_table(self):
        document = self.repo / "docs/skills.md"
        document.write_text("\n".join(line for line in document.read_text().splitlines() if not line.startswith("| [grill-me]")) + "\n")
        self.assert_graph_refused("grill-me: missing from the call-graph table")


if __name__ == "__main__":
    unittest.main()

