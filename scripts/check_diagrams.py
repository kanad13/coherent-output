#!/usr/bin/env python3
"""Check repository diagrams without traversing installed or local state.

Reuse the bundled skill checker so the standalone completion gate and edit
hooks agree on compilation and unavailable-tool results.
"""

import importlib.util
import os
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parent.parent


def main():
    """Check source Markdown and report the strongest checker failure.

    Returns:
        Zero for successful verification, one for invalid diagrams, or two
        when a required check cannot run.
    """
    source = REPO / "skills/mermaid-architect/scripts/verify-markdown.py"
    spec = importlib.util.spec_from_file_location("mermaid_verifier", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else REPO
    result = 0
    count = 0
    for directory, folders, files in os.walk(root):
        # evaluations is gitignored local review material holding deliberately invalid diagrams.
        folders[:] = [name for name in folders if name not in (".git", ".generated", "node_modules", "__pycache__", "evaluations")]
        for name in sorted(files):
            if Path(name).suffix.lower() in (".md", ".markdown"):
                count += 1
                code = module.verify_markdown_diagrams(Path(directory) / name)
                if code:
                    print(f"Diagram check failed: {Path(directory) / name}", file=sys.stderr)
                result = max(result, code)
    print(f"Checked diagrams in {count} Markdown files.")
    return result


if __name__ == "__main__":
    sys.exit(main())
