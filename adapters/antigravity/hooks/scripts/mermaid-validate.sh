#!/usr/bin/env bash
# Keep diagram compilation and dependency failures consistent across hosts.
set -euo pipefail
# GUI hosts do not load the user's shell profile.
export PATH="${PATH:-}:$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
exec python3 "$REPO_DIR/adapters/shared/document-check.py" --host antigravity --checks mermaid
