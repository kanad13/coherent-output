#!/usr/bin/env bash
# Supplement native approvals with conservative checks for common destructive forms.
set -euo pipefail
# GUI hosts do not load the user's shell profile.
export PATH="${PATH:-}:$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin"
exec python3 -c '
import json, re, shlex, sys
try:
    data = json.load(sys.stdin)
    command = data["toolCall"]["args"]["CommandLine"]
    if not isinstance(command, str) or not command.strip():
        raise ValueError("CommandLine must be a nonempty string")
    tokens = shlex.split(command)
    dangerous = bool(re.search(r"\bgit\s+(?:[^\n;&|]*\s)?(?:push\b[^\n;&|]*(?:--force(?:-with-lease)?\b|--delete\b|(?:^|\s)-[a-zA-Z]*f\b)|reset\s+--hard\b)|\bDROP\s+(?:DATABASE|TABLE)\b", command, re.I))
    for index, token in enumerate(tokens):
        if token == "rm" or token.endswith("/rm"):
            flags = []
            for item in tokens[index + 1:]:
                if item == "--":
                    break
                if item.startswith("-"):
                    flags.append(item)
            recursive = any(item in ("--recursive",) or (item.startswith("-") and not item.startswith("--") and "r" in item.lower()) for item in flags)
            forced = any(item == "--force" or (item.startswith("-") and not item.startswith("--") and "f" in item) for item in flags)
            dangerous |= recursive and forced
    decision = {"decision": "force_ask", "reason": "Destructive command pattern detected. Review with native approvals."} if dangerous else {"decision": "allow"}
except (ValueError, KeyError, TypeError):
    decision = {"decision": "force_ask", "reason": "Cannot inspect malformed command payload."}
print(json.dumps(decision))
'
