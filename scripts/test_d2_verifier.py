"""Check the d2-architect verifier: parsing, header rules, graph recovery, and real renders.

Unit cases need no D2. Render cases use the real compiler and skip, with the reason, when
none is provisioned, because a missing checker is an unavailable result and not a pass.
"""

import base64
import http.server
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest

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


class ContentRules(unittest.TestCase):
    """The user draws with shapes and labels only, on one board per block."""

    def errors(self, body):
        return verifier.static_checks(None, HEADER + body)[0]

    def test_icon_image_link_tooltip_and_import_fail(self):
        for body in ("x: X { icon: ./x.svg }\n", "x: X { shape: image }\n", "x: X { link: https://example.com }\n",
                     "x: X { tooltip: hi }\n", "...@other.d2\n", "layers: { a: { b } }\n"):
            with self.subTest(body=body):
                self.assertTrue(self.errors(body), body)

    def test_decorative_shapes_fail_but_data_shapes_pass(self):
        for shape in ("cylinder", "queue", "cloud", "diamond", "person", "document", "circle", "hexagon", "image"):
            with self.subTest(shape=shape):
                self.assertTrue(self.errors(f"x: X {{ shape: {shape} }}\n"), shape)
        for shape in ("sql_table", "class", "sequence_diagram", "rectangle"):
            with self.subTest(shape=shape):
                self.assertEqual(self.errors(f"x: X {{ shape: {shape} }}\n"), [], shape)

    def test_plain_shapes_and_classes_pass(self):
        self.assertEqual(self.errors("classes: { store: { style.stroke-dash: 4 } }\ndb: DB { class: store }\n"), [])


class StubService:
    """A d2-renderer look-alike on an ephemeral port that answers every POST with one status."""

    def __init__(self, status, body=b"<svg/>"):
        outer = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"OK")

            def do_POST(self):
                outer.received = self.rfile.read(int(self.headers["Content-Length"])).decode()
                outer.path = self.path
                self.send_response(status)
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *args):
                pass

        self.server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
        self.url = f"http://127.0.0.1:{self.server.server_port}"
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def close(self):
        self.server.shutdown()
        self.server.server_close()


class RenderService(unittest.TestCase):
    """Rendering through a d2-renderer service maps its answers onto the helper's statuses."""

    def render(self, status, body=b"<svg/>"):
        service = StubService(status, body)
        self.addCleanup(service.close)
        result = verifier.render(["@http", service.url + "/d2/svg"], "a -> b\n")
        return result, service

    def test_ok_sends_source_without_layout_flags(self):
        (state, svg, _), service = self.render(200, b"<svg>drawn</svg>")
        self.assertEqual((state, svg), ("ok", "<svg>drawn</svg>"))
        self.assertEqual(service.received, "a -> b\n")
        self.assertEqual(service.path, "/d2/svg")

    def test_compile_error_is_invalid_with_the_message(self):
        (state, _, message), _ = self.render(400, b"D2 Compilation Error:\nerr: -:3:1: bad")
        self.assertEqual(state, "invalid")
        self.assertIn("bad", message)

    def test_server_failure_is_unavailable_never_invalid(self):
        self.assertEqual(self.render(500)[0][0], "unavailable")
        self.assertEqual(self.render(504)[0][0], "unavailable")

    def test_unreachable_service_is_unavailable(self):
        self.assertEqual(verifier.render(["@http", "http://127.0.0.1:9/d2/svg"], "a -> b\n")[0], "unavailable")

    def test_renderer_selects_the_service_after_a_health_check(self):
        service = StubService(200)
        self.addCleanup(service.close)
        saved = os.environ.get("COHERENT_D2_RENDERER_URL")
        os.environ["COHERENT_D2_RENDERER_URL"] = service.url
        try:
            self.assertEqual(verifier.renderer(), ["@http", service.url + "/d2/svg"])
            os.environ["COHERENT_D2_RENDERER_URL"] = "http://127.0.0.1:9"
            with self.assertRaises(RuntimeError):
                verifier.renderer()
        finally:
            os.environ.pop("COHERENT_D2_RENDERER_URL", None)
            if saved is not None:
                os.environ["COHERENT_D2_RENDERER_URL"] = saved


class CliWithoutRenderer(unittest.TestCase):
    """The exit code is the contract: source violations are 1 and a missing renderer is 2."""

    def run_cli(self, block):
        env = {"PATH": "/nonexistent", "COHERENT_D2_RENDERER_URL": "http://127.0.0.1:9", "HOME": tempfile.gettempdir()}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "doc.md"
            path.write_text("# T\n\n**Diagram: A reaches B**\n\n```d2\n" + HEADER + block + "```\n", encoding="utf-8")
            return subprocess.run([sys.executable, "-I", str(SOURCE / "skills/d2-architect/scripts/verify-d2.py"), str(path)], capture_output=True, text=True, env=env).returncode

    def test_forbidden_content_exits_one_without_a_renderer(self):
        self.assertEqual(self.run_cli("a: A { icon: ./a.svg }\na -> b\n"), 1)
        self.assertEqual(self.run_cli("a: A { shape: cylinder }\na -> b\n"), 1)

    def test_clean_block_with_no_renderer_exits_two(self):
        self.assertEqual(self.run_cli("a -> b\n"), 2)


def svg_of(width, height):
    return f'<svg viewBox="0 0 {width} {height}"><svg viewBox="-25 -25 {width} {height}"></svg></svg>'


class RenderedSize(unittest.TestCase):
    """Strips and oversize pictures are what readers scroll and squint at."""

    def test_good_sizes_from_real_output_pass(self):
        for width, height in ((916, 842), (936, 998), (726, 674), (518, 908)):
            self.assertEqual(verifier.size_warnings(svg_of(width, height)), [], (width, height))

    def test_strips_and_oversize_warn(self):
        for width, height in ((212, 1520), (3140, 278), (328, 1131), (1841, 232), (1300, 700), (900, 1100), (1100, 300), (300, 950)):
            self.assertTrue(verifier.size_warnings(svg_of(width, height)), (width, height))

    def test_full_picture_gets_more_room_but_not_unlimited(self):
        self.assertEqual(verifier.size_warnings(svg_of(1314, 1119), full=True), [])
        self.assertEqual(verifier.size_warnings(svg_of(1252, 1679), full=True), [])
        self.assertTrue(verifier.size_warnings(svg_of(1900, 1000), full=True))

    def test_missing_viewbox_is_not_an_error(self):
        self.assertEqual(verifier.size_warnings("<svg></svg>"), [])

    def test_png_is_written_when_a_rasterizer_exists(self):
        if not verifier.rasterizer():
            self.skipTest("no rasterizer installed")
        with tempfile.TemporaryDirectory() as directory:
            svg, png = Path(directory) / "a.svg", Path(directory) / "a.png"
            svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 20"><rect width="40" height="20"/></svg>', encoding="utf-8")
            self.assertTrue(verifier.rasterize(svg, png, (40, 20)))
            self.assertTrue(png.read_bytes().startswith(b"\x89PNG"))


class SizeLimits(unittest.TestCase):
    def test_full_picture_caption_is_recognized(self):
        self.assertTrue(verifier.FULL_PICTURE.search("**Diagram 9: Full picture of the platform**"))
        self.assertFalse(verifier.FULL_PICTURE.search("**Diagram 9: Fulfilment reserves stock**"))


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

    def test_ladder_limit_is_fifteen_and_full_picture_is_forty(self):
        svg = "".join(group(f"n{i}") + group(f"(n{i} -&gt; n{i + 1})[0]") for i in range(19)) + group("n19")
        info = verifier.graph_from_svg(svg)
        self.assertTrue(any("limit 15" in w for w in verifier.graph_checks(info)[1]))
        self.assertEqual(verifier.graph_checks(info, full=True)[1], [])

    def test_version_parsing(self):
        self.assertEqual(verifier.parse_version("v0.9.0\n"), (0, 9, 0))
        self.assertIsNone(verifier.parse_version("none"))


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
