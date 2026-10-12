#!/usr/bin/env bash
# Thin launcher: GUI hosts do not load the shell profile, so locate Python here.
set -euo pipefail
export PATH="${PATH:-}:$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/../../../shared/safety-gate.py" --host antigravity
