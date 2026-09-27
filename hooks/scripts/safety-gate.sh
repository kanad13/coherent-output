#!/usr/bin/env bash
# Antigravity 2.0 PreToolUse hook script: inspects run_command for destructive operations.
set -euo pipefail

# Read stdin JSON payload
PAYLOAD=$(cat)

# Extract CommandLine from toolCall.args
CMD=$(echo "$PAYLOAD" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    cmd = data.get('toolCall', {}).get('args', {}).get('CommandLine', '')
    print(cmd)
except Exception:
    print('')
")

# Check for high-risk destructive patterns (case-insensitive)
if echo "$CMD" | grep -Eiq '(git\s+push\s+.*(-f\b|--force)|git\s+push\s+.*--delete|git\s+reset\s+--hard|rm\s+-[a-zA-Z]*r[a-zA-Z]*f[a-zA-Z]*\s+[/~]|rm\s+-[a-zA-Z]*f[a-zA-Z]*r[a-zA-Z]*\s+[/~]|DROP\s+DATABASE|DROP\s+TABLE)'; then
  echo '{"decision": "force_ask", "reason": "Destructive command pattern detected. Explicit user approval required."}'
else
  echo '{"decision": "allow"}'
fi
