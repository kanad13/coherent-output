#!/usr/bin/env bash
# verify.sh: Single-command validation runner for deployment sync, test suites, and formatting.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "=== 1. Checking Deployment & Sync ==="
python3 "$REPO_DIR/scripts/deploy.py" --check

echo "=== 2. Running Test Suite ==="
python3 "$REPO_DIR/scripts/test_deploy.py"

echo "=== 3. Checking Prettier Formatting ==="
npx prettier --check "$REPO_DIR"

echo "=== All Verification Checks Passed ==="
