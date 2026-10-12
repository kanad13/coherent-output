#!/usr/bin/env python3
"""Ask for native review before common destructive shell forms run.

One pattern list serves every host; only the payload field and the verdict
envelope differ. The gate is conservative pattern matching, not a shell
interpreter or a security boundary, so native permissions remain necessary.
"""

import argparse
import json
import re
import shlex
import sys

DESTRUCTIVE_GIT_OR_SQL = re.compile(
    r"\bgit\s+(?:[^\n;&|]*\s)?(?:push\b[^\n;&|]*(?:--force(?:-with-lease)?\b|--delete\b|(?:^|\s)-[a-zA-Z]*f\b)|reset\s+--hard\b)"
    r"|\bDROP\s+(?:DATABASE|TABLE)\b",
    re.I,
)


def command_of(payload, host):
    """Read the shell command from a host payload.

    Args:
        payload: Native hook event as a JSON object.
        host: ``antigravity`` or ``claude``.

    Returns:
        The command string.

    Raises:
        ValueError: The command is absent, not a string, or empty.
    """
    if host == "antigravity":
        command = payload["toolCall"]["args"]["CommandLine"]
    else:
        command = payload["tool_input"]["command"]
    if not isinstance(command, str) or not command.strip():
        raise ValueError("command must be a nonempty string")
    return command


def is_destructive(command):
    """Detect forced pushes, hard resets, dropped data, and recursive forced removal.

    Args:
        command: Shell command text, inspected but never executed.

    Returns:
        Whether the command matches a destructive pattern.

    Raises:
        ValueError: The command cannot be tokenized.
    """
    dangerous = bool(DESTRUCTIVE_GIT_OR_SQL.search(command))
    tokens = shlex.split(command)
    for index, token in enumerate(tokens):
        if token == "rm" or token.endswith("/rm"):
            flags = []
            for item in tokens[index + 1:]:
                if item == "--":
                    break
                if item.startswith("-"):
                    flags.append(item)
            short = [item for item in flags if not item.startswith("--")]
            recursive = "--recursive" in flags or any("r" in item.lower() for item in short)
            forced = "--force" in flags or any("f" in item for item in short)
            dangerous |= recursive and forced
    return dangerous


def verdict(host, ask, reason):
    """Render the host's review request, or its no-opinion result.

    Args:
        host: ``antigravity`` or ``claude``.
        ask: Whether to request review.
        reason: Explanation shown with the request.

    Returns:
        JSON text for stdout, or an empty string when Claude Code should apply
        its normal permission flow.
    """
    if host == "antigravity":
        return json.dumps({"decision": "force_ask", "reason": reason} if ask else {"decision": "allow"})
    if not ask:
        return ""  # Silence leaves Claude Code's own permission rules in charge.
    return json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse", "permissionDecision": "ask", "permissionDecisionReason": reason,
    }})


def main():
    """Classify one hook event from stdin.

    Returns:
        Zero; a malformed payload is a review request, never a crash.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", required=True, choices=("antigravity", "claude"))
    host = parser.parse_args().host
    try:
        ask = is_destructive(command_of(json.load(sys.stdin), host))
        reason = "Destructive command pattern detected. Review with native approvals."
    except (ValueError, KeyError, TypeError):
        ask, reason = True, "Cannot inspect malformed command payload."
    output = verdict(host, ask, reason)
    if output:
        print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
