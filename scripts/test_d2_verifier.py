"""Check the d2-architect verifier: parsing, header rules, graph recovery, and real renders.

Unit cases need no D2. Render cases use the real compiler and skip, with the reason, when
none is provisioned, because a missing checker is an unavailable result and not a pass.
"""

import base64
import http.server
import importlib.util
from pathlib import Path
import tempfile
import threading
import unittest
from unittest import mock

SOURCE = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("d2_verifier", SOURCE / "skills/d2-architect/scripts/verify-d2.py")
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)

HEADER = "vars: {\n  d2-config: {\n    layout-engine: tala\n    theme-id: 0\n    dark-theme-id: 200\n  }\n}\n"
DOCUMENT = (
    "# Title\n\nIntro.\n\n**Diagram: A reaches B**\n\n```d2\n" + HEADER + "a -> b\n```\n\n"
    "## Example\n\n```text\n```d2\nnot a diagram\n```\n```\n"
)


def group(path):
    """Build the SVG group D2 emits for a resolved path."""
    return f'<g class="{base64.b64encode(path.encode()).decode()}">'


class ParsingAndHeader(unittest.TestCase):
    """Pin block detection and the TALA header rule."""

    def test_only_real_d2_fences_are_parsed(self):
        blocks, unclosed = verifier.parse_blocks(DOCUMENT)
        self.assertEqual(len(blocks), 1)
        self.assertFalse(unclosed)
        self.assertEqual(blocks[0]["heading"], "Title")
        self.assertEqual(blocks[0]["caption"], "**Diagram: A reaches B**")

    def test_unclosed_fence_is_reported(self):
        self.assertTrue(verifier.parse_blocks("# T\n\n```d2\na -> b\n")[1])

    def test_missing_header_is_an_error(self):
        errors, _ = verifier.static_checks(None, "a -> b")
        self.assertTrue(any("layout-engine" in e for e in errors))

    def test_other_engine_is_an_error(self):
        errors, _ = verifier.static_checks(None, HEADER.replace("tala", "elk") + "a -> b")
        self.assertTrue(any("must use tala" in e for e in errors))

    def test_tala_header_passes_and_color_override_warns(self):
        self.assertEqual(verifier.static_checks(None, HEADER + "a -> b")[0], [])
        warnings = verifier.static_checks(None, HEADER + "a: A { style.fill: red }\nx: X {\n  style: {\n    fill: red\n  }\n}")[1]
        self.assertTrue(any("override" in w for w in warnings))

    def test_compound_caption_warns(self):
        self.assertTrue(verifier.static_checks("**Diagram: A feeds B, while C feeds D**", HEADER)[1])


class GraphRecovery(unittest.TestCase):
    """Recover nodes, containers, and edges from the group names D2 writes."""

    def test_connected_container_graph(self):
        svg = "".join(group(p) for p in ["user", "platform", "platform.api", "platform.db", "platform.(api -&gt; db)[0]", "(user -&gt; platform.api)[0]"])
        info = verifier.graph_from_svg(svg)
        self.assertEqual(info["containers"], {"platform"})
        self.assertIn(("platform.api", "platform.db"), info["edges"])
        self.assertIn(("user", "platform.api"), info["edges"])
        self.assertEqual(verifier.graph_checks(info)[0], [])

    def test_sequence_lifelines_are_not_nodes_or_islands(self):
        names = ["flow", "flow.tv", "flow.as", "(flow.tv -- )[0]", "(flow.as -- )[0]", "flow.(tv -&gt; as)[0]", "flow.(as -&gt; tv)[0]"]
        info = verifier.graph_from_svg("".join(group(p) for p in names))
        self.assertEqual(sorted(info["nodes"]), ["flow", "flow.as", "flow.tv"])
        self.assertEqual(verifier.graph_checks(info)[0], [])

    def test_islands_are_an_error(self):
        svg = "".join(group(p) for p in ["a", "b", "c", "d", "(a -&gt; b)[0]", "(c -&gt; d)[0]"])
        errors, _ = verifier.graph_checks(verifier.graph_from_svg(svg))
        self.assertTrue(any("disconnected" in e for e in errors))

    def test_large_graph_warns(self):
        svg = "".join(group(f"n{i}") + group(f"(n{i} -&gt; n{i + 1})[0]") for i in range(45)) + group("n45")
        self.assertTrue(any("nodes" in w for w in verifier.graph_checks(verifier.graph_from_svg(svg))[1]))

    def test_remote_icon_is_a_static_error(self):
        errors, _ = verifier.static_checks(None, HEADER + "x: X { icon: https://icons.example.invalid/x.svg }")
        self.assertTrue(any("remote icon" in e for e in errors))


class FakeRenderer(http.server.BaseHTTPRequestHandler):
    """Stand in for the d2-renderer service: the contract the helper relies on."""

    server_version = "D2Renderer/1.0"
    health_body = b"OK"

    def log_message(self, *args):
        pass

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Length", str(len(self.health_body)))
        self.end_headers()
        self.wfile.write(self.health_body)

    def do_POST(self):
        source = self.rfile.read(int(self.headers["Content-Length"])).decode()
        if "boom" in source:
            code, body = 500, b"D2 compiler binary 'd2' not found"
        elif "bad" in source:
            code, body = 400, b"D2 Compilation Error:\nerr: failed to compile: -:3:1: unexpected text"
        else:
            code, body = 200, b"<svg/>"
        self.send_response(code)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


class ServiceBackend(unittest.TestCase):
    """Check renderer selection and the service reply mapping without D2 installed."""

    def serve(self, body=b"OK"):
        handler = type("Handler", (FakeRenderer,), {"health_body": body})
        server = http.server.HTTPServer(("127.0.0.1", 0), handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.shutdown)
        self.addCleanup(server.server_close)
        return f"http://127.0.0.1:{server.server_port}"

    def test_running_service_is_chosen_first(self):
        url = self.serve()
        with mock.patch.object(verifier, "SERVICE_URL", url), mock.patch.object(verifier.shutil, "which", return_value=None):
            self.assertEqual(verifier.renderer(), ("service", url))

    def test_other_server_on_the_port_is_not_trusted(self):
        url = self.serve(body=b"something else")
        with mock.patch.object(verifier, "SERVICE_URL", url), mock.patch.object(verifier.shutil, "which", return_value=None):
            with self.assertRaises(RuntimeError):
                verifier.renderer()

    def test_no_service_and_no_docker_is_unavailable(self):
        with mock.patch.object(verifier, "SERVICE_URL", "http://127.0.0.1:9"), mock.patch.object(verifier.shutil, "which", return_value=None):
            with self.assertRaises(RuntimeError):
                verifier.renderer()
            self.assertEqual(verifier.verify_blocks([{"caption": None, "heading": "T", "code": HEADER + "a -> b"}]), 2)

    def test_service_reply_codes_map_to_status(self):
        backend = ("service", self.serve())
        self.assertEqual(verifier.render(backend, "a -> b")[0], "ok")
        status, _, message = verifier.render(backend, "bad", palette="x: 1\n")
        self.assertEqual(status, "invalid")
        self.assertIn("-:2:1", message)  # the palette line is subtracted
        self.assertEqual(verifier.render(backend, "boom")[0], "unavailable")

    def test_environment_does_not_select_a_renderer(self):
        with mock.patch.dict(verifier.os.environ, {"COHERENT_D2_BIN": "/bin/echo"}), \
                mock.patch.object(verifier, "SERVICE_URL", "http://127.0.0.1:9"), mock.patch.object(verifier.shutil, "which", return_value=None):
            with self.assertRaises(RuntimeError):
                verifier.renderer()


class RealRenders(unittest.TestCase):
    """Exercise the compiler through the CLI contract."""

    @classmethod
    def setUpClass(cls):
        try:
            cls.command = verifier.renderer()
        except (OSError, RuntimeError) as error:
            raise unittest.SkipTest(f"D2 not provisioned: {error}")

    def run_markdown(self, content):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "doc.md"
            path.write_text(content, encoding="utf-8")
            return verifier.verify_blocks(verifier.parse_blocks(path.read_text(encoding="utf-8"))[0])

    def test_valid_diagram_passes(self):
        self.assertEqual(self.run_markdown("# T\n\n```d2\n" + HEADER + "a -> b\n```\n"), 0)

    def test_syntax_error_is_invalid(self):
        self.assertEqual(self.run_markdown("# T\n\n```d2\n" + HEADER + "a -> {\n```\n"), 1)

    def test_island_is_invalid(self):
        self.assertEqual(self.run_markdown("# T\n\n```d2\n" + HEADER + "a -> b\nc -> d\n```\n"), 1)

    def test_remote_icon_is_invalid_not_unavailable(self):
        block = HEADER + "x: X { icon: https://icons.example.invalid/x.svg }\n"
        self.assertEqual(self.run_markdown("# T\n\n```d2\n" + block + "```\n"), 1)

    def test_sequence_diagram_passes(self):
        block = HEADER + "flow: Flow {\n  shape: sequence_diagram\n  a: A\n  b: B\n  a -> b: ask\n  b -> a: answer\n}\n"
        self.assertEqual(self.run_markdown("# T\n\n```d2\n" + block + "```\n"), 0)

    def test_palette_composes_with_block_config(self):
        palette = (SOURCE / "skills/d2-architect/assets/house-palette.d2").read_text(encoding="utf-8")
        status, svg, _ = verifier.render(self.command, HEADER + "a -> b\n", palette)
        self.assertEqual(status, "ok")
        self.assertIn("#2563EB", svg)
        self.assertNotIn("#0D32B2", svg)

    def test_error_lines_ignore_the_palette_prefix(self):
        palette = (SOURCE / "skills/d2-architect/assets/house-palette.d2").read_text(encoding="utf-8")
        status, _, message = verifier.render(self.command, HEADER + "a -> {\n", palette)
        self.assertEqual(status, "invalid")
        self.assertIn("-:8:", message)

    def test_document_without_d2_needs_no_renderer(self):
        self.assertEqual(verifier.verify_blocks([]), 0)


if __name__ == "__main__":
    unittest.main()
