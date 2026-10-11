#!/usr/bin/env bash
# Resolve this checkout without copying machine-owned application state.
set -euo pipefail
# Agent runtimes may not load the user's shell profile.
export PATH="${PATH:-}:$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin"

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 "$REPO_DIR/scripts/deploy.py" "$@"
