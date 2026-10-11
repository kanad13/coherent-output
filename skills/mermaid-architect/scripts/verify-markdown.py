#!/usr/bin/env python3
"""Compile Mermaid diagrams with a provisioned, version-checked renderer.

The helper travels with the skill. It never downloads a dependency during a
check, and distinguishes invalid diagrams from unavailable tooling.
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
                result = subprocess.run(
                    [binary, "-i", str(source), "-o", str(output), "-e", "svg", "--quiet"],
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


def verify_markdown_diagrams(file_path):
    """Check fenced diagrams without changing the surrounding document.

    Args:
        file_path: Path to a UTF-8 Markdown document.

    Returns:
        Zero for no diagrams or successful compilation, one for an unclosed
        fence or recognized syntax failure, or two for unavailable verification.
    """
    try:
        content = file_path.read_text(encoding="utf-8")
    except OSError as error:
        print(f"Cannot read diagram source: {error}", file=sys.stderr)
        return 2
    diagrams = []
    fence = None
    lines = []
    for line in content.splitlines():
        if fence is None:
            opening = re.match(r"^ {0,3}(`{3,}|~{3,})mermaid\s*$", line)
            if opening:
                fence = opening.group(1)
                lines = []
        elif re.match(r"^ {0,3}" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*$", line):
            diagrams.append("\n".join(lines))
            fence = None
        else:
            lines.append(line)
    if fence:
        print("Unclosed Mermaid fence.", file=sys.stderr)
        return 1
    return compile_diagrams(diagrams)


def main():
    """Expose the same verification statuses for raw diagrams and Markdown.

    Returns:
        The checker status: zero, one, or two.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--diagram", action="store_true", help="Compile a raw .mmd input instead of Markdown fences")
    args = parser.parse_args()
    if args.diagram:
        try:
            return compile_diagrams([args.source.read_text(encoding="utf-8")])
        except OSError as error:
            print(f"Cannot read diagram source: {error}", file=sys.stderr)
            return 2
    return verify_markdown_diagrams(args.source)


if __name__ == "__main__":
    sys.exit(main())
