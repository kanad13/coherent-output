#!/usr/bin/env bash
# Antigravity 2.0 PostToolUse hook script: batch validates Mermaid diagrams in modified Markdown files.
set -euo pipefail

# Read stdin JSON payload
PAYLOAD=$(cat)

# Extract and sanitize TargetFile from toolCall.args
TARGET_FILE=$(echo "$PAYLOAD" | python3 -c "
import sys, json, os
try:
    data = json.load(sys.stdin)
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

if [ -n "$TARGET_FILE" ] && [ -f "$TARGET_FILE" ]; then
  case "$TARGET_FILE" in
    *.md|*.markdown)
      if grep -q '```mermaid' "$TARGET_FILE"; then
        SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        REPO_DIR="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
        VERIFY_SCRIPT="$REPO_DIR/skills/mermaid-architect/scripts/verify-markdown.py"
        if [ -f "$VERIFY_SCRIPT" ]; then
          python3 "$VERIFY_SCRIPT" "$TARGET_FILE"
        fi
      fi
      ;;
  esac
fi

# PostToolUse contract requires stdout to be valid JSON: {}
echo '{}'
