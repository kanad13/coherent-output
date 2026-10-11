#!/usr/bin/env python3
"""Normalize host edit payloads and provide observable document-check feedback.

Host schemas stay at this boundary. The installed tools run locally without
downloads; post-edit feedback reports failures but cannot undo an edit.
"""

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys

REPO = Path(__file__).resolve().parents[2]
os.environ["PATH"] = os.pathsep.join([os.environ.get("PATH", ""), str(Path.home() / ".local/bin"), "/opt/homebrew/bin", "/usr/local/bin"])
FORMAT_SUFFIXES = {".md", ".markdown", ".mdx", ".json", ".jsonc", ".json5", ".yaml", ".yml", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".css", ".scss", ".html", ".htm", ".vue", ".graphql", ".gql"}


def edited_paths(payload, host):
    """Extract supported edit paths without guessing at shell write effects.

    Args:
        payload: Native hook event as a JSON object.
        host: Host contract, either ``codex`` or ``antigravity``.

    Returns:
        Resolved paths with supported extensions; failed Antigravity events and
        Codex Bash events produce no paths.

    Raises:
        ValueError: The supported event's required fields are malformed.
    """
    if not isinstance(payload, dict):
        raise ValueError("Hook input must be a JSON object.")
    cwd = payload.get("cwd") or str(Path.cwd())
    if not isinstance(cwd, str):
        raise ValueError("Hook cwd must be a string.")
    if host == "antigravity":
        if payload.get("error"):
            return []
        call = payload.get("toolCall", {})
        if isinstance(call, dict) and call.get("error"):
            return []
        args = call.get("args", {}) if isinstance(call, dict) else {}
        raw = args.get("TargetFile") if isinstance(args, dict) else None
        if not isinstance(raw, str) or not raw:
            raise ValueError("Antigravity write payload requires toolCall.args.TargetFile.")
        paths = [raw]
    else:
        name = payload.get("tool_name")
        if name == "Bash":
            return []  # Shell writes need the standalone verification gate.
        args = payload.get("tool_input", {})
        if not isinstance(args, dict):
            raise ValueError("Codex tool_input must be an object.")
        if name == "apply_patch":
            command = args.get("command")
            if not isinstance(command, str):
                raise ValueError("Codex apply_patch input requires command.")
            paths = re.findall(r"^\*\*\* (?:Add File|Update File|Move to): (.+)$", command, re.MULTILINE)
            moved = set(re.findall(r"^\*\*\* Update File: (.+)\n\*\*\* Move to:", command, re.MULTILINE))
            paths = [item for item in paths if item not in moved]
        elif name in ("Edit", "Write"):
            paths = [args.get("file_path")]
            if not isinstance(paths[0], str) or not paths[0]:
                raise ValueError("Codex Edit/Write input requires file_path.")
        else:
            raise ValueError(f"Unsupported Codex tool: {name!r}")
    normalized = []
    for raw in paths:
        if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in ("'", '"'):
            raw = raw[1:-1]
        target = Path(raw).expanduser()
        if not target.is_absolute():
            target = Path(cwd) / target
        if target.suffix.lower() in FORMAT_SUFFIXES and target not in normalized:
            normalized.append(target.resolve())
    return normalized


def project_prettier(target):
    """Respect project tooling before falling back to this library's formatter.

    Args:
        target: Resolved edited-file path.

    Returns:
        The nearest installed Prettier executable, or the library's fallback.

    Raises:
        RuntimeError: No installed formatter is available.
    """
    for parent in target.parents:
        executable = parent / "node_modules/.bin/prettier"
        if executable.is_file():
            return executable
    executable = REPO / "node_modules/.bin/prettier"
    if executable.is_file():
        return executable
    raise RuntimeError("Prettier unavailable. Run npm ci in the coherent-output checkout.")


def format_file(target):
    """Format in the project's ignore context with its configuration preferred.

    Args:
        target: Resolved edited-file path to format in place.

    Raises:
        OSError: The formatter cannot be launched.
        RuntimeError: Configuration discovery or formatting fails.
        subprocess.TimeoutExpired: Discovery or formatting exceeds its limit.
    """
    executable = project_prettier(target)
    command = [str(executable), "--write", str(target)]
    config = subprocess.run([str(executable), "--find-config-path", str(target)], cwd=target.parent, capture_output=True, text=True, timeout=10)
    no_config = config.returncode == 1 and "Can not find configure file" in config.stderr
    if not no_config and (config.returncode or config.stderr.strip()):
        raise RuntimeError(config.stderr.strip() or "Cannot resolve Prettier configuration.")
    if not config.stdout.strip():
        command += ["--config", str(REPO / ".prettierrc")]
    project_root = next((parent for parent in target.parents if any((parent / marker).exists() for marker in (".prettierignore", ".git"))), None)
    if project_root is None:
        project_root = next((parent for parent in target.parents if (parent / "package.json").is_file()), None)
    if project_root is None:
        project_root = Path(config.stdout.strip()).parent if config.stdout.strip() else target.parent
    result = subprocess.run(command, cwd=project_root, capture_output=True, text=True, timeout=20)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or f"Prettier exited {result.returncode}.")
    if result.stdout.strip():
        print(result.stdout.strip(), file=sys.stderr)


def check_file(target, checks):
    """Expose unavailable or failed checks rather than silently accepting edits.

    Args:
        target: Resolved edited-file path.
        checks: ``all``, ``format``, or ``mermaid``; diagram checks apply only
            to Markdown files.

    Raises:
        ValueError: The edited file is unavailable.
        RuntimeError: A requested checker fails or is unavailable.
        OSError: A checker cannot be launched.
        subprocess.TimeoutExpired: A checker exceeds its execution limit.
    """
    if not target.is_file():
        raise ValueError(f"Edited file is unavailable for checking: {target}")
    if checks in ("all", "format"):
        format_file(target)
    if checks in ("all", "mermaid") and target.suffix.lower() in (".md", ".markdown"):
        verifier = REPO / "skills/mermaid-architect/scripts/verify-markdown.py"
        result = subprocess.run([sys.executable, str(verifier), str(target)], capture_output=True, text=True, timeout=75)
        if result.returncode:
            raise RuntimeError(result.stderr.strip() or f"Mermaid checker exited {result.returncode}.")
        if result.stdout.strip():
            print(result.stdout.strip(), file=sys.stderr)


def main():
    """Normalize stdin and emit feedback for the selected native host.

    Returns:
        Zero after successful checks, or two with visible failure feedback.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", required=True, choices=("codex", "antigravity"))
    parser.add_argument("--checks", choices=("all", "format", "mermaid"), default="all")
    args = parser.parse_args()
    try:
        for target in edited_paths(json.load(sys.stdin), args.host):
            check_file(target, args.checks)
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as error:
        reason = f"Document check failed: {error}"
        print(reason, file=sys.stderr)
        if args.host == "codex":
            print(json.dumps({"decision": "block", "reason": reason}))
        else:
            print("{}")
        return 2
    print("{}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
