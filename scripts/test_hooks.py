"""Exercise real file effects and failure feedback across supported hook contracts.

Temporary documents keep formatter writes isolated. Real renderer checks prove
compilation; controlled missing-tool cases prove that unavailable checks fail.
"""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parent.parent
CHECKER = SOURCE / "adapters/shared/document-check.py"
VERIFIER = SOURCE / "skills/mermaid-architect/scripts/verify-markdown.py"


class DocumentHookTests(unittest.TestCase):
    """Establish actual checker effects and failure feedback on isolated files."""

    def setUp(self):
        """Create disposable documents so formatting cannot change user data."""
        self.temporary = tempfile.TemporaryDirectory(prefix="coherent-hook-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.sample = self.root / "file with space's.md"
        self.sample.write_text("#  Header\n\n-  item\n")

    def check(self, host, payload, checks="all", env=None):
        """Run the shared boundary with the same JSON contract as a host hook.

        Args:
            host: Native host contract to exercise.
            payload: Hook event serialized to stdin.
            checks: Requested checker selection.
            env: Optional child environment for controlled runtime failures.

        Returns:
            The completed checker process, including status and feedback.
        """
        return subprocess.run(
            [sys.executable, str(CHECKER), "--host", host, "--checks", checks],
            input=json.dumps(payload), capture_output=True, text=True, env=env, timeout=100,
        )

    def test_codex_patch_formats_multiple_files_relative_to_payload_cwd(self):
        second = self.root / "other.json"
        second.write_text('{"ok":true}\n')
        command = f"*** Begin Patch\n*** Update File: {self.sample.name}\n@@\n*** Add File: other.json\n*** End Patch"
        result = self.check("codex", {"cwd": str(self.root), "tool_name": "apply_patch", "tool_input": {"command": command}})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {})
        self.assertEqual(self.sample.read_text(), "# Header\n\n- item\n")
        self.assertEqual(json.loads(second.read_text()), {"ok": True})
        self.assertIn('"ok": true', second.read_text())

    def test_codex_patch_move_checks_destination_after_source_is_gone(self):
        command = f"*** Begin Patch\n*** Update File: gone.md\n*** Move to: {self.sample.name}\n@@\n*** End Patch"
        result = self.check("codex", {"cwd": str(self.root), "tool_name": "apply_patch", "tool_input": {"command": command}})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.sample.read_text(), "# Header\n\n- item\n")

    def test_claude_edit_write_and_multiedit_use_file_path(self):
        for tool in ("Edit", "Write", "MultiEdit"):
            with self.subTest(tool=tool):
                self.sample.write_text("#  Header\n\n-  item\n")
                result = self.check("claude", {"tool_name": tool, "tool_input": {"file_path": str(self.sample)}})
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(self.sample.read_text(), "# Header\n\n- item\n")

    def test_claude_failure_uses_exit_two_without_json_on_stdout(self):
        sample = self.root / "invalid.json"
        sample.write_text("{broken")
        result = self.check("claude", {"tool_name": "Write", "tool_input": {"file_path": str(sample)}})
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("Document check failed", result.stderr)

    def test_shell_coverage_is_explicitly_outside_path_extraction(self):
        result = self.check("codex", {"tool_name": "Bash", "tool_input": {"command": "pwd"}})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.sample.read_text(), "#  Header\n\n-  item\n")

    def test_antigravity_formats_actual_content_with_quoted_path(self):
        result = self.check("antigravity", {"toolCall": {"args": {"TargetFile": f'"{self.sample}"'}}})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {})
        self.assertEqual(self.sample.read_text(), "# Header\n\n- item\n")

    @unittest.skipUnless(sys.platform == "darwin", "Mac host PATH contract")
    def test_gui_style_path_resolves_provisioned_node(self):
        env = {**os.environ, "PATH": "/usr/bin:/bin:/usr/sbin:/sbin"}
        result = self.check("antigravity", {"toolCall": {"args": {"TargetFile": str(self.sample)}}}, env=env)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.sample.read_text(), "# Header\n\n- item\n")

    def test_prettier_ignore_protects_exact_table_text(self):
        table = "| Stage | Owner |\n| --- | --- |\n| Store | Worker |\n"
        self.sample.write_text("#  Header\n\n<!-- prettier-ignore -->\n" + table)
        result = self.check("codex", {"tool_name": "Write", "tool_input": {"file_path": str(self.sample)}})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(table, self.sample.read_text())
        self.assertTrue(self.sample.read_text().startswith("# Header\n"))

    def test_monorepo_root_ignore_survives_nested_package(self):
        (self.root / ".prettierignore").write_text("packages/pkg/generated/\n")
        package = self.root / "packages/pkg"
        package.mkdir(parents=True)
        (package / "package.json").write_text("{}")
        sample = package / "generated/example.js"
        sample.parent.mkdir()
        original = 'const greeting="hello";\n'
        sample.write_text(original)
        result = self.check("antigravity", {"toolCall": {"args": {"TargetFile": str(sample)}}})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(sample.read_text(), original)

    def test_existing_project_config_controls_formatting(self):
        (self.root / ".prettierrc").write_text('{"singleQuote": true, "semi": false}')
        sample = self.root / "sample.js"
        sample.write_text('const greeting="hello";\n')
        result = self.check("antigravity", {"toolCall": {"args": {"TargetFile": str(sample)}}})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(sample.read_text(), "const greeting = 'hello'\n")

    def test_json5_config_and_markdown_extension_are_supported(self):
        (self.root / ".prettierrc.json5").write_text("{singleQuote: true, semi: false}")
        script = self.root / "sample.js"
        script.write_text('const greeting="hello";\n')
        markdown = self.sample.with_suffix(".markdown")
        markdown.write_text("#  Header\n\n-  item\n")
        for sample in (script, markdown):
            result = self.check("antigravity", {"toolCall": {"args": {"TargetFile": str(sample)}}})
            self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(script.read_text(), "const greeting = 'hello'\n")
        self.assertEqual(markdown.read_text(), "# Header\n\n- item\n")

    def test_project_ignore_and_failed_edit_leave_existing_file_intact(self):
        (self.root / ".prettierignore").write_text("ignored/\n")
        sample = self.root / "ignored/generated.js"
        sample.parent.mkdir()
        original = 'const greeting="hello";\n'
        sample.write_text(original)
        result = self.check("antigravity", {"toolCall": {"args": {"TargetFile": str(sample)}}})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(sample.read_text(), original)
        result = self.check("antigravity", {"error": "edit failed", "toolCall": {"args": {"TargetFile": str(self.sample)}}})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.sample.read_text(), "#  Header\n\n-  item\n")

    def test_missing_browser_is_unavailable_not_a_syntax_error(self):
        self.sample.write_text("```mermaid\nflowchart LR\n A-->B\n```\n")
        env = {**os.environ, "PUPPETEER_EXECUTABLE_PATH": str(self.root / "missing-browser")}
        result = subprocess.run([sys.executable, str(VERIFIER), str(self.sample)], capture_output=True, text=True, env=env)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("verification unavailable", result.stderr)

    def test_prettier_error_produces_failed_codex_feedback(self):
        sample = self.root / "invalid.json"
        sample.write_text("{broken")
        result = self.check("codex", {"tool_name": "Write", "tool_input": {"file_path": str(sample)}})
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["decision"], "block")
        self.assertIn("Document check failed", result.stderr)

    def test_malformed_payloads_are_not_successful_checks(self):
        for host in ("codex", "claude", "antigravity"):
            with self.subTest(host=host):
                result = self.check(host, {})
                self.assertEqual(result.returncode, 2)
                self.assertIn("Document check failed", result.stderr)

    def test_valid_and_invalid_mermaid_produce_different_results(self):
        for diagram, expected in (("flowchart LR\n A-->B", 0), ("flowchart LR\n A-->", 2)):
            with self.subTest(diagram=diagram):
                self.sample.write_text("```mermaid\n" + diagram + "\n```\n")
                result = self.check("antigravity", {"toolCall": {"args": {"TargetFile": str(self.sample)}}}, checks="mermaid")
                self.assertEqual(result.returncode, expected, result.stderr)
                self.assertEqual(json.loads(result.stdout), {})
                if expected:
                    self.assertIn("failed compilation", result.stderr)

    def test_missing_renderer_is_reported_and_non_mermaid_needs_no_renderer(self):
        env = {**os.environ, "COHERENT_MMDC_BIN": str(self.root / "missing-mmdc")}
        self.sample.write_text("```mermaid\nflowchart LR\n A-->B\n```\n")
        result = self.check("codex", {"tool_name": "Write", "tool_input": {"file_path": str(self.sample)}}, checks="mermaid", env=env)
        self.assertEqual(result.returncode, 2)
        self.assertIn("unavailable", result.stderr)
        self.assertEqual(json.loads(result.stdout)["decision"], "block")
        self.sample.write_text("# No diagrams\n")
        standalone = subprocess.run([sys.executable, str(VERIFIER), str(self.sample)], capture_output=True, text=True, env=env)
        self.assertEqual(standalone.returncode, 0, standalone.stderr)

    def test_renderer_version_mismatch_fails_and_does_not_compile(self):
        fake = self.root / "mmdc"
        fake.write_text("#!/bin/sh\necho 0.0.0\n")
        fake.chmod(0o755)
        self.sample.write_text("```mermaid\nflowchart LR\n A-->B\n```\n")
        env = {**os.environ, "COHERENT_MMDC_BIN": str(fake)}
        result = subprocess.run([sys.executable, str(VERIFIER), str(self.sample)], capture_output=True, text=True, env=env)
        self.assertEqual(result.returncode, 2)
        self.assertIn("must be 12.0.0", result.stderr)

    def test_raw_diagram_helper_runs_outside_checkout_and_cleans_temporary_files(self):
        diagram = self.root / "input.mmd"
        diagram.write_text("flowchart LR\n A-->B\n")
        temporary = self.root / "scratch"
        temporary.mkdir()
        result = subprocess.run(
            ["bash", str(VERIFIER.with_name("verify-mmdc.sh")), str(diagram)],
            cwd=self.root, capture_output=True, text=True, env={**os.environ, "TMPDIR": str(temporary)}, timeout=75,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(list(temporary.iterdir()), [])

    def test_missing_prettier_returns_failure(self):
        isolated = self.root / "isolated"
        script = isolated / "adapters/shared/document-check.py"
        script.parent.mkdir(parents=True)
        script.write_text(CHECKER.read_text())
        result = subprocess.run(
            [sys.executable, str(script), "--host", "antigravity", "--checks", "format"],
            input=json.dumps({"toolCall": {"args": {"TargetFile": str(self.sample)}}}),
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("Prettier unavailable", result.stderr)


class SafetyGateTests(unittest.TestCase):
    """Verify review decisions without executing the submitted command strings."""
    def test_common_variants_and_malformed_input_request_review(self):
        script = SOURCE / "adapters/antigravity/hooks/scripts/safety-gate.sh"
        samples = [
            ("pwd", "allow"), ("git status", "allow"),
            ("git reset --hard", "force_ask"), ("git -C ./repo push origin --force", "force_ask"),
            ("rm -rf ./relative", "force_ask"), ("rm -r -f /example", "force_ask"),
            ("rm --recursive --force /example", "force_ask"), ("rm -fr ~/example", "force_ask"),
            ("DROP TABLE events", "force_ask"),
        ]
        for command, expected in samples:
            with self.subTest(command=command):
                result = subprocess.run(["bash", str(script)], input=json.dumps({"toolCall": {"args": {"CommandLine": command}}}), text=True, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout)["decision"], expected)
        result = subprocess.run(["bash", str(script)], input="not-json", text=True, capture_output=True)
        self.assertEqual(json.loads(result.stdout)["decision"], "force_ask")


if __name__ == "__main__":
    unittest.main()
