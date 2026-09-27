#!/usr/bin/env bash
# Antigravity 2.0 PostToolUse hook script: auto-formats files edited by write_to_file / replace_file_content with Prettier.
set -euo pipefail

# Read stdin JSON payload
PAYLOAD=$(cat)

# Extract TargetFile from toolCall.args
TARGET_FILE=$(echo "$PAYLOAD" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    # Check if there was an error in tool execution
    if data.get('error'):
        sys.exit(0)
    args = data.get('toolCall', {}).get('args', {})
    target = args.get('TargetFile', '')
    print(target)
except Exception:
    pass
")

# If file exists and prettier is available, run prettier
if [ -n "$TARGET_FILE" ] && [ -f "$TARGET_FILE" ]; then
  case "$TARGET_FILE" in
    *.md|*.markdown|*.json|*.yaml|*.yml|*.js|*.ts|*.jsx|*.tsx|*.html|*.css)
      if command -v prettier &>/dev/null; then
        prettier --write "$TARGET_FILE" --ignore-unknown --log-level error 2>/dev/null || true
      fi
      ;;
  esac
fi

# PostToolUse contract requires stdout to be valid JSON: {}
echo '{}'
