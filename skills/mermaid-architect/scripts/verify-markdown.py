#!/usr/bin/env python3
"""Compile Mermaid diagrams with a provisioned, version-checked renderer.

The helper travels with the skill. It never downloads a dependency during a
check, and distinguishes invalid diagrams from unavailable tooling.

Structure checks run before rendering because they need no browser and catch
defects that compile cleanly (disconnected groups, reversed direction); a
structure error therefore fails fast with exit code 1.
"""

import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

MMDC_VERSION = "12.0.0"
os.environ["PATH"] = os.pathsep.join([os.environ.get("PATH", ""), str(Path.home() / ".local/bin"), "/opt/homebrew/bin", "/usr/local/bin"])


def renderer():
    """Verify provisioned tooling without downloading during an edit check.

    Returns:
        The executable path for the required Mermaid CLI version.

    Raises:
        RuntimeError: The renderer is absent, fails, or has the wrong version.
        OSError: The renderer cannot be launched.
        subprocess.TimeoutExpired: Version discovery exceeds ten seconds.
    """
    explicit = os.environ.get("COHERENT_MMDC_BIN")
    candidates = [Path(explicit)] if explicit else [
        Path(__file__).resolve().parents[3] / "node_modules/.bin/mmdc",
        Path(__file__).resolve().parents[1] / "node_modules/.bin/mmdc",
    ]
    binary = next((str(item) for item in candidates if item.is_file()), None)
    if not binary and not explicit:
        binary = shutil.which("mmdc")
    if not binary:
        raise RuntimeError(f"Mermaid CLI unavailable. Provision @mermaid-js/mermaid-cli@{MMDC_VERSION}; no diagrams were verified.")
    result = subprocess.run([binary, "--version"], capture_output=True, text=True, timeout=10)
    if result.returncode or result.stdout.strip() != MMDC_VERSION:
        raise RuntimeError(f"Mermaid CLI must be {MMDC_VERSION}; received {result.stdout.strip()!r}.")
    return binary

MAX_NODES = 10
MAX_SUBGRAPHS = 3
FORBIDDEN_DIRECTIONS = ("RL", "BT")
COMPOUND = re.compile(r"(,\s*(while|whereas|but|and)\b|\b(while|whereas|meanwhile|although)\b|;|\bas well as\b)", re.I)
ODD_SHAPE = re.compile(r"\w(?:\(\[|\[\(|\{\{|\[\[|\(\(|\{|\(|>|\[/|\[\\)")
ARROW = re.compile(r"\s*(?:<?-\.+-+>?|<?-{2,}>?|<?={2,}>?)\s*")
KEYWORDS = ("flowchart", "graph", "classdef", "class ", "style ", "linkstyle", "direction", "%%", "click ")


def parse_blocks(content):
    """Return ((caption, code) pairs, unclosed) for every Mermaid fence, in document order.

    The caption is the nearest non-blank line above the fence, or None.
    """
    blocks, fence, lines, last = [], None, [], None
    for line in content.splitlines():
        if fence is None:
            opening = re.match(r"^ {0,3}(`{3,}|~{3,})mermaid\s*$", line)
            if opening:
                fence, lines = opening.group(1), []
            elif line.strip():
                last = line.strip()
        elif re.match(r"^ {0,3}" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*$", line):
            blocks.append((last, "\n".join(lines)))
            fence, last = None, None
        else:
            lines.append(line)
    return blocks, fence is not None


def parse_flowchart(code):
    """Extract nodes, edges, subgraph membership and direction from a flowchart.

Args:
    code: Mermaid flowchart source.

Returns:
    Dict with node and subgraph id sets, edge pairs, a child-to-subgraph map, and the direction.
"""
    nodes, edges, subs, parent = set(), [], set(), {}
    stack = []
    direction = None
    for raw in code.splitlines():
        line = raw.strip().rstrip(";")
        head = re.match(r"^(?:flowchart|graph)\s+(TD|TB|LR|RL|BT)\b", line)
        if head:
            direction = head.group(1)
            continue
        sub = re.match(r'^subgraph\s+([\w-]+)?\s*(?:\[.*\])?\s*$', line) or re.match(r'^subgraph\s+"(.*)"$', line)
        if sub:
            sid = sub.group(1) or f"anon{len(subs)}"
            subs.add(sid)
            if stack:
                parent[sid] = stack[-1]
            stack.append(sid)
            continue
        if line == "end":
            if stack:
                stack.pop()
            continue
        if not line or line.lower().startswith(KEYWORDS):
            continue
        text = re.sub(r"(--|==)\s*\"[^\"]*\"\s*(-->|==>|---)", r"\2", line)
        text = re.sub(r'"[^"]*"', "Q", text)
        text = re.sub(r"\|[^|]*\|", "", text)
        text = re.sub(r"\[\[[^\]]*\]\]|\[[^\]]*\]|\{[^}]*\}|\(\([^)]*\)\)|\([^)]*\)", "", text)
        text = re.sub(r":::\w+", "", text)
        parts = [p.strip() for p in ARROW.split(text)]
        groups = [[i for i in re.findall(r"[A-Za-z_][\w-]*", p)] for p in parts]
        for group in groups:
            for ident in group:
                nodes.add(ident)
                if stack and ident not in subs:
                    parent.setdefault(ident, stack[-1])
        for left, right in zip(groups, groups[1:]):
            edges += [(a, b) for a in left for b in right]
    return {"nodes": nodes, "edges": edges, "subs": subs, "parent": parent,
            "direction": direction}


def components(items, links):
    """Group items joined by links.

    Args:
        items: Iterable of hashable ids.
        links: Pairs of ids that belong together; unknown ids are ignored.

    Returns:
        A list of sets, one per connected group.
    """
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


def check_structure(caption, code):
    """Return (errors, warnings) for one diagram without launching a browser.

Args:
    caption: The caption line above the fence, or None.
    code: Mermaid source of the diagram.

Returns:
    Two lists of messages. Errors fail verification; warnings fail only under --strict.
"""
    errors, warnings = [], []
    kind = code.strip().split()[0] if code.strip() else ""
    if caption and COMPOUND.search(caption):
        warnings.append("compound caption: one diagram carries one idea; split it or state the single relation")
    if kind == "sequenceDiagram" and re.search(r"^\s*\S.*?(->>|-->>|->|-->).*?:\s*\"", code, re.M):
        warnings.append("quotes render literally in sequence messages; remove them")
    if kind not in ("flowchart", "graph"):
        return errors, warnings
    for line in code.splitlines():
        text = line.strip()
        if text.startswith(KEYWORDS) or text.lower().startswith(KEYWORDS):
            continue
        text = re.sub(r"\|[^|]*\|", "", re.sub(r'"[^"]*"', "Q", text))
        if ODD_SHAPE.search(text):
            errors.append(f"node shape other than a plain box: {line.strip()[:70]!r}; draw every node as A[\"Label\"]")
            break
    info = parse_flowchart(code)
    if info["direction"] in FORBIDDEN_DIRECTIONS:
        errors.append(f"direction {info['direction']} puts consumers before sources; use LR or TD")
    members = info["nodes"] - info["subs"]
    if len(members) > MAX_NODES:
        errors.append(f"{len(members)} nodes exceed the limit of {MAX_NODES}")
    if len(info["subs"]) > MAX_SUBGRAPHS:
        errors.append(f"{len(info['subs'])} subgraphs exceed the limit of {MAX_SUBGRAPHS}")
    universe = info["nodes"] | info["subs"]
    # Membership counts as a relation: boxes are the author's explicit grouping.
    links = list(info["edges"]) + [(n, p) for n, p in info["parent"].items()]
    parts = components(universe, links)
    if len(parts) > 1:
        sizes = sorted((len(p) for p in parts), reverse=True)
        errors.append(f"disconnected diagram: {len(parts)} separate groups ({sizes}); join them with a hub, a labelled edge, or one named outer box")
    return errors, warnings


def compile_diagrams(diagrams):
    """Compile inputs without leaking temporary files or hiding runtime gaps.

    Args:
        diagrams: Sequence of Mermaid source strings to compile.

    Returns:
        Zero for no inputs or successful compilation, one for recognized
        syntax failures, or two when verification is unavailable.
    """
    if not diagrams:
        return 0
    try:
        binary = renderer()
        with tempfile.TemporaryDirectory(prefix="coherent-mermaid-") as directory:
            for index, code in enumerate(diagrams, start=1):
                source = Path(directory) / f"diagram-{index}.mmd"
                output = source.with_suffix(".svg")
                source.write_text(code, encoding="utf-8")
                command = [binary, "-i", str(source), "-o", str(output), "-e", "svg", "--quiet"]
                # CI runners need browser flags such as --no-sandbox that the library cannot guess.
                if os.environ.get("COHERENT_PUPPETEER_CONFIG"):
                    command += ["-p", os.environ["COHERENT_PUPPETEER_CONFIG"]]
                result = subprocess.run(
                    command,
                    capture_output=True, text=True, timeout=60,
                )
                if result.returncode or not output.is_file():
                    diagnostic = result.stderr.strip() or result.stdout.strip()
                    syntax_error = any(marker in diagnostic.lower() for marker in ("parse error", "syntax error", "lexical error", "unknowndiagramerror", "no diagram type detected"))
                    classification = "invalid diagram" if syntax_error else "verification unavailable"
                    print(f"Diagram {index} failed compilation ({classification}): {diagnostic}", file=sys.stderr)
                    return 1 if syntax_error else 2
        print(f"Verified {len(diagrams)} Mermaid diagram(s).")
        return 0
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as error:
        print(f"Mermaid verification unavailable: {error}", file=sys.stderr)
        return 2


def verify_markdown_diagrams(file_path, strict=False):
    """Check fenced diagrams without changing the surrounding document.

    Args:
        file_path: Path to a UTF-8 Markdown document.
        strict: Treat warnings (compound caption, quoted sequence messages) as failures.

    Returns:
        Zero for no diagrams or successful compilation, one for an unclosed
        fence, structure error, or recognized syntax failure, or two for
        unavailable verification.
    """
    try:
        content = file_path.read_text(encoding="utf-8")
    except OSError as error:
        print(f"Cannot read diagram source: {error}", file=sys.stderr)
        return 2
    blocks, unclosed = parse_blocks(content)
    if unclosed:
        print("Unclosed Mermaid fence.", file=sys.stderr)
        return 1
    warnings, failed = [], False
    for index, (caption, code) in enumerate(blocks, start=1):
        errors, warns = check_structure(caption, code)
        for message in errors:
            print(f"Diagram {index} structure error: {message}", file=sys.stderr)
        warnings += [f"diagram {index}: {w}" for w in warns]
        failed = failed or bool(errors)
    if failed:
        for message in warnings:
            print(f"Warning: {message}", file=sys.stderr)
        return 1
    result = compile_diagrams([code for _, code in blocks])
    for message in warnings:
        print(f"Warning: {message}", file=sys.stderr)
    return 1 if result == 0 and warnings and strict else result


def main():
    """Expose the same verification statuses for raw diagrams and Markdown.

    Returns:
        The checker status: zero, one, or two.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    parser.add_argument("--diagram", action="store_true", help="Compile a raw .mmd input instead of Markdown fences")
    args = parser.parse_args()
    if args.diagram:
        try:
            return compile_diagrams([args.source.read_text(encoding="utf-8")])
        except OSError as error:
            print(f"Cannot read diagram source: {error}", file=sys.stderr)
            return 2
    return verify_markdown_diagrams(args.source, args.strict)


if __name__ == "__main__":
    sys.exit(main())
