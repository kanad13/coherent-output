#!/usr/bin/env bash
# verify.sh: Single-command validation runner for deployment sync, test suites, and formatting.
set -euo pipefail
# Agent runtimes may not load the user's shell profile.
export PATH="${PATH:-}:$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin"

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "=== 1. Checking Deployment & Sync ==="
python3 "$REPO_DIR/scripts/deploy.py" --check "$@"

echo "=== 2. Running Behavior Tests ==="
python3 -m unittest discover -s "$REPO_DIR/scripts" -p 'test_*.py'

echo "=== 3. Checking Prettier Formatting ==="
"$REPO_DIR/node_modules/.bin/prettier" --check "$REPO_DIR"

echo "=== 4. Checking Repository Diagrams ==="
python3 "$REPO_DIR/scripts/check_diagrams.py" "$REPO_DIR"

echo "=== All Verification Checks Passed ==="
