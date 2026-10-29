"""Check the d2-architect verifier: parsing, header rules, graph recovery, and real renders.

Unit cases need no D2. Render cases use the real compiler and skip, with the reason, when
none is provisioned, because a missing checker is an unavailable result and not a pass.
"""

import base64
import importlib.util
from pathlib import Path
import tempfile
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

    def test_plain_shapes_and_classes_pass(self):
        self.assertEqual(self.errors("classes: { store: { shape: cylinder } }\ndb: DB { class: store }\n"), [])


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
