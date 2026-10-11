#!/usr/bin/env bash
# Share renderer checks and temporary-file cleanup with the bundled Python helper.
set -euo pipefail
# Agent runtimes may not load the user's shell profile.
export PATH="${PATH:-}:$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/verify-markdown.py" --diagram "$@"
