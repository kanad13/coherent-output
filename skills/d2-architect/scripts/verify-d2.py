#!/usr/bin/env python3
"""Compile D2 diagrams with a version-checked renderer and report what was drawn.

The helper travels with the skill. It never downloads a dependency during a check and
distinguishes invalid diagrams (exit 1) from unavailable tooling (exit 2).

Each block is rendered WITHOUT a layout flag: a flag would override the block's own
`layout-engine`, hiding a missing or wrong setting. The compiled SVG also names every
shape and connection, so connectivity is checked on what D2 resolved, not on a guess
from the source text. Optionally the run writes a contact sheet so a reviewer can look
at every diagram, which no exit code can replace, and prepends a palette file so the
sheet shows the house look. D2 merges repeated `vars` blocks, so the palette composes
with each block's own d2-config.
"""

import argparse
import base64
import html
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request

D2_IMAGE = "d2lang/d2:v0.9.0"
MIN_VERSION = (0, 9, 0)
RENDER_TIMEOUT = 90
LADDER_NODE_LIMIT = 15
FULL_NODE_LIMIT = 40
os.environ["PATH"] = os.pathsep.join([os.environ.get("PATH", ""), str(Path.home() / ".local/bin"), "/opt/homebrew/bin", "/usr/local/bin"])

COMPOUND = re.compile(r"(,\s*(while|whereas|but|and)\b|\b(while|whereas|meanwhile|although)\b|;|\bas well as\b)", re.I)
HEADING = re.compile(r"^ {0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
OPENING = re.compile(r"^ {0,3}(`{3,}|~{3,})\s*([\w-]*)")
CONNECTION = re.compile(r"^(?:(?P<prefix>.*)\.)?\((?P<left>.+?) (?P<arrow><->|->|<-|--) (?P<right>.*?)\)\[\d+\]$")
COLOR_OVERRIDE = re.compile(r"^\s*(fill|stroke|font-color)\s*:\s*[\"']?(#|[a-zA-Z])", re.M)
# The user draws with shapes and labels only. Remote assets also fail the offline render, but a
# local icon path or a link compiles, so the source text is checked directly.
FORBIDDEN = (
    (re.compile(r"(?:^|[{;.])\s*icon\s*:", re.M), "`icon` is not allowed: diagrams carry meaning in shapes and labels"),
    (re.compile(r"shape\s*:\s*[\"']?(?!(?:sql_table|class|sequence_diagram|rectangle)\b)\w", re.M), "only plain boxes are allowed: `shape:` may be sql_table, class, or sequence_diagram"),
    (re.compile(r"(?:^|[{;.])\s*(link|tooltip)\s*:", re.M), "`link` and `tooltip` are not allowed: static previews drop them"),
    (re.compile(r"^\s*(\.\.\.)?\s*@", re.M), "imports are not allowed: a block must be self-contained"),
    (re.compile(r"(?:^|[{;.])\s*(layers|scenarios|steps)\s*:", re.M), "`layers`, `scenarios` and `steps` are not allowed: a fence shows only the root board; use one block per level"),
)
FULL_PICTURE = re.compile(r"full picture", re.I)


def parse_version(text):
    """Extract a (major, minor, patch) tuple from `d2 --version` output, or None."""
    found = re.search(r"(\d+)\.(\d+)\.(\d+)", text)
    return tuple(int(part) for part in found.groups()) if found else None


def renderer():
    """Locate a D2 renderer without downloading anything.

    Order: a running d2-renderer service named by COHERENT_D2_RENDERER_URL, explicit COHERENT_D2_BIN, a `d2` on PATH, then the pinned Docker image run
    with networking disabled so remote icons cannot make a block pass here and fail
    elsewhere.

    Returns:
        The argument list that, followed by `- -`, renders stdin to stdout, or
        ["@http", url] for a d2-renderer service.

    Raises:
        RuntimeError: No renderer is available or the version is too old.
        OSError: A candidate cannot be launched.
        subprocess.TimeoutExpired: Version discovery exceeds ten seconds.
    """
    service = os.environ.get("COHERENT_D2_RENDERER_URL")
    if service:
        base = service.rstrip("/")
        try:
            with urllib.request.urlopen(base + "/health", timeout=10) as reply:
                reply.read()
        except (OSError, urllib.error.URLError) as error:
            raise RuntimeError(f"COHERENT_D2_RENDERER_URL {service!r} is not answering: {error}")
        return ["@http", base + "/d2/svg"]
    explicit = os.environ.get("COHERENT_D2_BIN")
    binary = explicit or shutil.which("d2")
    if binary:
        result = subprocess.run([binary, "--version"], capture_output=True, text=True, timeout=10)
        version = parse_version(result.stdout + result.stderr)
        if version and version >= MIN_VERSION:
            return [binary]
        if explicit:
            raise RuntimeError(f"D2 must be v{'.'.join(map(str, MIN_VERSION))} or later (TALA is bundled from that release); received {result.stdout.strip()!r}.")
    docker = shutil.which("docker")
    if docker:
        probe = subprocess.run([docker, "image", "inspect", D2_IMAGE], capture_output=True, timeout=30)
        if probe.returncode == 0:
            return [docker, "run", "--rm", "-i", "--network", "none", "--entrypoint", "d2", D2_IMAGE]
    raise RuntimeError(f"D2 unavailable. Provision it with `docker pull {D2_IMAGE}` or `brew install d2` (v0.9.0 or later); no diagrams were verified.")


def parse_blocks(content):
    """Return (blocks, unclosed) for every d2 fence, in document order.

    Fences of other languages are skipped whole, so a d2 example inside a text fence is
    not mistaken for a diagram.

    Args:
        content: Markdown source.

    Returns:
        A list of dicts with `caption` (nearest non-blank line above the fence, or None),
        `heading` (nearest heading above), `code`, and the boolean `unclosed`.
    """
    blocks, fence, language, lines = [], None, None, []
    caption, heading = None, None
    for line in content.splitlines():
        if fence is None:
            opening = OPENING.match(line)
            if opening:
                fence, language, lines = opening.group(1), opening.group(2).lower(), []
                continue
            title = HEADING.match(line)
            if title:
                heading, caption = title.group(2), None
            elif line.strip():
                caption = line.strip()
        elif re.match(r"^ {0,3}" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*$", line):
            if language == "d2":
                blocks.append({"caption": caption, "heading": heading, "code": "\n".join(lines)})
            fence, caption = None, None
        else:
            lines.append(line)
    return blocks, fence is not None and language == "d2"


def static_checks(caption, code):
    """Check what the source text alone can show.

    Args:
        caption: The caption line above the fence, or None.
        code: D2 source of the diagram.

    Returns:
        (errors, warnings). Errors fail verification; warnings fail only under --strict.
    """
    errors, warnings = [], []
    engine = re.search(r"layout-engine\s*:\s*[\"']?(\w+)", code)
    if not engine:
        errors.append("missing `layout-engine: tala` in the standard d2-config header")
    elif engine.group(1) != "tala":
        errors.append(f"layout-engine is {engine.group(1)}; every block must use tala")
    errors.extend(message for pattern, message in FORBIDDEN if pattern.search(code))
    if caption and COMPOUND.search(caption):
        warnings.append("compound caption: one diagram carries one idea; split it or state the single relation")
    if COLOR_OVERRIDE.search(code):
        warnings.append("fill, stroke or font-color override: fixed colors break contrast in the other color scheme; let the theme color it")
    return errors, warnings


def decode_class(value):
    """Decode a D2 SVG group class into a path, or None when it is not a D2 name."""
    try:
        text = base64.b64decode(value + "=" * (-len(value) % 4), validate=True).decode("utf-8")
    except (ValueError, UnicodeDecodeError):
        return None
    return html.unescape(text)


def graph_from_svg(svg):
    """Recover shapes, containers and connections from a compiled D2 SVG.

    D2 names every group by the base64 of its resolved path, for example `platform.api`
    or `platform.(api -> db)[0]`, so the drawn graph is read back exactly.

    Args:
        svg: SVG text produced by D2.

    Returns:
        Dict with `nodes` (shape paths), `containers` (paths that hold other shapes),
        and `edges` (pairs of full endpoint paths).
    """
    nodes, edges = [], []
    for value in re.findall(r'<g class="([^"]+)"', svg):
        path = decode_class(value)
        if path is None or not path:
            continue
        link = CONNECTION.match(path)
        if link and not link.group("right"):
            continue  # a sequence-diagram lifeline: it has a start but no destination
        if link:
            prefix = (link.group("prefix") or "") + "."
            prefix = "" if prefix == "." else prefix
            edges.append((prefix + link.group("left"), prefix + link.group("right")))
        elif value not in ("shape", "connection"):
            nodes.append(path)
    unique = list(dict.fromkeys(nodes))
    containers = {n for n in unique if any(other.startswith(n + ".") for other in unique)}
    return {"nodes": unique, "containers": containers, "edges": edges}


def components(items, links):
    """Group items joined by links; unknown ids in links are ignored."""
    root = {i: i for i in items}

    def find(i):
        while root[i] != i:
            root[i] = root[root[i]]
            i = root[i]
        return i
    for a, b in links:
        if a in root and b in root:
            root[find(a)] = find(b)
    groups = {}
    for i in items:
        groups.setdefault(find(i), set()).add(i)
    return list(groups.values())


def graph_checks(info, full=False):
    """Check the drawn graph for the structural rules the skill sets.

    Args:
        info: Result of graph_from_svg.
        full: True for a "Full picture" diagram, which may hold more nodes.

    Returns:
        (errors, warnings).
    """
    errors, warnings = [], []
    nodes = info["nodes"]
    leaves = [n for n in nodes if n not in info["containers"]]
    limit = FULL_NODE_LIMIT if full else LADDER_NODE_LIMIT
    if len(leaves) > limit:
        warnings.append(f"{len(leaves)} nodes (limit {limit}): readers lose the thread; zoom into one part per diagram or, for a Full picture diagram, split it")
    # Membership counts as a relation: a container is the author's explicit grouping.
    membership = [(n, n.rsplit(".", 1)[0]) for n in nodes if "." in n]
    parts = components(nodes, list(info["edges"]) + membership)
    if len(parts) > 1:
        sizes = sorted((len(p) for p in parts), reverse=True)
        errors.append(f"disconnected diagram: {len(parts)} separate groups ({sizes}); join them with a hub, a labelled edge, or one named outer container")
    return errors, warnings


def shift_lines(message, offset):
    """Rewrite `-:LINE:COL` positions so they point into the block, not the palette prefix."""
    return re.sub(r"-:(\d+):(\d+)", lambda m: f"-:{max(int(m.group(1)) - offset, 1)}:{m.group(2)}", message)


def render_over_http(url, source, offset):
    """Render through a d2-renderer service, which compiles offline and sends no layout flag.

    The service answers 400 with the compiler message for invalid D2, so that maps to
    "invalid"; any other failure means the service cannot be used.
    """
    request = urllib.request.Request(url, data=source.encode("utf-8"), method="POST")
    try:
        with urllib.request.urlopen(request, timeout=RENDER_TIMEOUT) as reply:
            return "ok", reply.read().decode("utf-8"), ""
    except urllib.error.HTTPError as error:
        message = shift_lines(error.read().decode("utf-8", errors="replace").strip(), offset)
        return ("invalid" if error.code == 400 else "unavailable"), "", message
    except (OSError, urllib.error.URLError) as error:
        return "unavailable", "", f"render service failed: {error}"


def render(command, code, palette=""):
    """Render one block with the block's own configuration.

    Args:
        command: Renderer prefix from renderer().
        code: D2 source.
        palette: Optional D2 text prepended before rendering (the house palette).

    Returns:
        (status, svg, diagnostic) where status is "ok", "invalid" or "unavailable".
    """
    env = {key: value for key, value in os.environ.items() if not key.startswith("D2_")}
    source = palette + code if not palette or palette.endswith("\n") else palette + "\n" + code
    offset = source.count("\n") - code.count("\n")
    if command[0] == "@http":
        return render_over_http(command[1], source, offset)
    try:
        result = subprocess.run(command + ["-", "-"], input=source.encode("utf-8"), capture_output=True, timeout=RENDER_TIMEOUT, env=env)
    except subprocess.TimeoutExpired:
        return "unavailable", "", f"render exceeded {RENDER_TIMEOUT}s"
    stderr = shift_lines(result.stderr.decode("utf-8", errors="replace").strip(), offset)
    if result.returncode == 0 and result.stdout:
        return "ok", result.stdout.decode("utf-8"), stderr
    # "failed to bundle" means the block fetches a remote asset; the offline render rejects it by design.
    markers = ("failed to compile", "failed to parse", "failed to bundle", "failed to fully compile", "is not a valid", "expected", "unexpected", "invalid")
    if any(marker in stderr.lower() for marker in markers):
        return "invalid", "", stderr
    return "unavailable", "", stderr or "renderer exited without output"


def write_sheet(directory, entries):
    """Write rendered SVGs and an index.html contact sheet for visual review.

    Args:
        directory: Existing or creatable output directory.
        entries: List of dicts with number, heading, caption, code, svg.

    Returns:
        The path of index.html.
    """
    out = Path(directory)
    out.mkdir(parents=True, exist_ok=True)
    cards = []
    for entry in entries:
        name = f"diagram-{entry['number']}.svg"
        (out / name).write_text(entry["svg"], encoding="utf-8")
        cards.append(
            f'<section><h2>#{entry["number"]} {html.escape(entry["heading"] or "(no heading)")}</h2>'
            f'<p class="cap">{html.escape(entry["caption"] or "(no caption)")}</p>'
            f'<img src="{name}" alt="diagram {entry["number"]}">'
            f'<details><summary>source</summary><pre>{html.escape(entry["code"])}</pre></details></section>'
        )
    page = (
        '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>D2 contact sheet</title>'
        '<style>:root{color-scheme:light dark}body{font:14px system-ui,sans-serif;margin:24px;background:Canvas;color:CanvasText}'
        'section{border:1px solid #8886;border-radius:6px;padding:12px;margin:0 0 20px}h2{font-size:15px;margin:0 0 4px}'
        '.cap{margin:0 0 8px;opacity:.8}img{display:block;margin:0 auto;max-width:100%;max-height:640px}pre{overflow:auto}</style></head><body>'
        f'<h1>D2 contact sheet ({len(entries)} diagrams)</h1>' + "".join(cards) + "</body></html>"
    )
    index = out / "index.html"
    index.write_text(page, encoding="utf-8")
    return index


def verify_blocks(blocks, strict=False, sheet=None, palette=""):
    """Verify a list of parsed blocks.

    Args:
        blocks: Dicts from parse_blocks.
        strict: Treat warnings as failures.
        sheet: Directory for the contact sheet, or None.
        palette: D2 text prepended to every render, or "".

    Returns:
        Zero when every block passes, one for invalid diagrams or structure, two when
        verification could not run.
    """
    if not blocks:
        return 0
    # Source rules need no renderer, so a violation is reported as invalid (1), not unavailable (2).
    early = False
    for number, block in enumerate(blocks, start=1):
        for message in static_checks(block["caption"], block["code"])[0]:
            print(f"Diagram {number} error: {message}", file=sys.stderr)
            early = True
    if early:
        return 1
    try:
        command = renderer()
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as error:
        print(f"D2 verification unavailable: {error}", file=sys.stderr)
        return 2
    failed, warned, entries = False, False, []
    for number, block in enumerate(blocks, start=1):
        errors, warnings = static_checks(block["caption"], block["code"])
        status, svg, diagnostic = render(command, block["code"], palette)
        if status == "unavailable":
            print(f"Diagram {number}: verification unavailable: {diagnostic}", file=sys.stderr)
            return 2
        if status == "invalid":
            errors.append(f"does not compile: {diagnostic}")
        else:
            more_errors, more_warnings = graph_checks(graph_from_svg(svg), full=bool(block["caption"] and FULL_PICTURE.search(block["caption"])))
            errors, warnings = errors + more_errors, warnings + more_warnings
            entries.append({"number": number, "heading": block["heading"], "caption": block["caption"], "code": block["code"], "svg": svg})
        for message in errors:
            print(f"Diagram {number} error: {message}", file=sys.stderr)
        for message in warnings:
            print(f"Diagram {number} warning: {message}", file=sys.stderr)
        failed, warned = failed or bool(errors), warned or bool(warnings)
    if sheet and entries:
        print(f"Contact sheet: {write_sheet(sheet, entries)}")
    if failed or (strict and warned):
        return 1
    print(f"Verified {len(blocks)} D2 diagram(s).")
    return 0


def main():
    """Expose one status contract for raw diagrams and Markdown documents.

    Returns:
        The checker status: zero, one, or two.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    parser.add_argument("--diagram", action="store_true", help="Treat the input as one raw .d2 diagram instead of Markdown")
    parser.add_argument("--sheet", type=Path, help="Write a contact sheet (index.html and SVGs) to this directory")
    parser.add_argument("--palette", type=Path, help="D2 file prepended to every render, such as assets/house-palette.d2, to preview the house look")
    args = parser.parse_args()
    try:
        content = args.source.read_text(encoding="utf-8")
    except OSError as error:
        print(f"Cannot read diagram source: {error}", file=sys.stderr)
        return 2
    if args.diagram:
        blocks = [{"caption": None, "heading": args.source.name, "code": content}]
    else:
        blocks, unclosed = parse_blocks(content)
        if unclosed:
            print("Unclosed d2 fence.", file=sys.stderr)
            return 1
    palette = ""
    if args.palette:
        try:
            palette = args.palette.read_text(encoding="utf-8")
        except OSError as error:
            print(f"Cannot read palette: {error}", file=sys.stderr)
            return 2
    return verify_blocks(blocks, args.strict, args.sheet, palette)


if __name__ == "__main__":
    sys.exit(main())
