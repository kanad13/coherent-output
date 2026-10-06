#!/usr/bin/env python3
"""Batch verify all Mermaid code blocks embedded inside a Markdown document."""

import argparse
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


def verify_markdown_diagrams(file_path: Path) -> int:
    if not file_path.is_file():
        print(f"Error: Target file not found: {file_path}", file=sys.stderr)
        return 1

    if not shutil.which("npx"):
        print("Warning: npx not installed. Skipping headless mmdc compilation check.")
        return 0

    content = file_path.read_text(encoding="utf-8")
    pattern = re.compile(r"```mermaid\r?\n([\s\S]*?)```")
    matches = list(pattern.finditer(content))

    if not matches:
        print(f"No Mermaid diagram blocks found in {file_path.name}.")
        return 0

    print(f"Verifying {len(matches)} Mermaid diagram(s) in {file_path.name}...")
    errors = 0

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        for index, match in enumerate(matches, start=1):
            diagram_code = match.group(1).strip()
            mmd_file = temp_path / f"diag_{index}.mmd"
            svg_file = temp_path / f"diag_{index}.svg"
            mmd_file.write_text(diagram_code, encoding="utf-8")

            cmd = [
                "npx",
                "-y",
                "@mermaid-js/mermaid-cli",
                "-i",
                str(mmd_file),
                "-o",
                str(svg_file),
                "-e",
                "svg",
                "--quiet",
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"  ✓ Diagram {index}: Compilation SUCCESS")
            else:
                print(f"  ✗ Diagram {index}: Compilation FAILED!", file=sys.stderr)
                if result.stderr.strip():
                    print(f"    {result.stderr.strip()}", file=sys.stderr)
                errors += 1

    if errors > 0:
        print(f"Verification failed: {errors} diagram(s) had syntax errors.", file=sys.stderr)
        return 1

    print(f"Success: All {len(matches)} diagram(s) compiled cleanly.")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("markdown_file", type=Path, help="Path to markdown file containing Mermaid blocks")
    args = parser.parse_args()
    sys.exit(verify_markdown_diagrams(args.markdown_file))


if __name__ == "__main__":
    main()
