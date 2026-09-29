#!/usr/bin/env bash
# Antigravity 2.0 PostToolUse hook script: auto-formats files edited by write_to_file / replace_file_content with Prettier.
set -euo pipefail

# Read stdin JSON payload
PAYLOAD=$(cat)

# Extract and sanitize TargetFile from toolCall.args
TARGET_FILE=$(echo "$PAYLOAD" | python3 -c "
import sys, json, os
try:
    data = json.load(sys.stdin)
    # Check if there was an error in tool execution
    if data.get('error'):
        sys.exit(0)
    args = data.get('toolCall', {}).get('args', {})
    target = args.get('TargetFile') or args.get('target_file') or args.get('path') or args.get('filePath') or ''
    if isinstance(target, str):
        target = target.strip().strip('\"\'').strip()
        if target:
            print(os.path.expanduser(target))
except Exception:
    pass
")

# Ensure user and package-manager binaries are available in PATH
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"

# If file exists and prettier is available, run prettier
if [ -n "$TARGET_FILE" ] && [ -f "$TARGET_FILE" ]; then
  case "$TARGET_FILE" in
    *.md|*.markdown|*.json|*.yaml|*.yml|*.js|*.ts|*.jsx|*.tsx|*.html|*.css)
      PRETTIER_BIN=""
      if command -v prettier &>/dev/null; then
        PRETTIER_BIN="prettier"
      elif command -v npx &>/dev/null; then
        PRETTIER_BIN="npx prettier"
      fi

      if [ -n "$PRETTIER_BIN" ]; then
        SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        REPO_DIR="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
        REPO_CONFIG="$REPO_DIR/.prettierrc"

        if [ -f "$REPO_CONFIG" ] && ! $PRETTIER_BIN --find-config-path "$TARGET_FILE" &>/dev/null; then
          $PRETTIER_BIN --write --config "$REPO_CONFIG" "$TARGET_FILE" --ignore-unknown --log-level error 2>/dev/null || true
        else
          $PRETTIER_BIN --write "$TARGET_FILE" --ignore-unknown --log-level error 2>/dev/null || true
        fi
      fi
      ;;
  esac
fi

# PostToolUse contract requires stdout to be valid JSON: {}
echo '{}'
