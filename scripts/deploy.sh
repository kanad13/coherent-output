#!/usr/bin/env bash
# deploy.sh: Idempotently deploys coherent-output customizations into ~/.gemini/config/ via symlinks.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_CONFIG_DIR="$HOME/.gemini/config"
TARGET_GEMINI_DIR="$HOME/.gemini"

echo "=== Deploying Antigravity 2.0 Customizations from $REPO_DIR ==="

mkdir -p "$TARGET_CONFIG_DIR"

link_item() {
  local src="$1"
  local dest="$2"

  if [ -L "$dest" ]; then
    local current_target
    current_target="$(readlink "$dest")"
    if [ "$current_target" = "$src" ]; then
      echo "  [OK] Symlink already configured: $dest -> $src"
      return 0
    else
      echo "  [UPDATE] Updating symlink: $dest (was -> $current_target)"
      rm -f "$dest"
    fi
  elif [ -e "$dest" ]; then
    echo "  [BACKUP] Backing up existing destination: $dest -> ${dest}.bak"
    mv "$dest" "${dest}.bak"
  fi

  ln -s "$src" "$dest"
  echo "  [CREATED] Linked $dest -> $src"
}

# 1. Global Persona & Invariants
link_item "$REPO_DIR/AGENTS.md" "$TARGET_GEMINI_DIR/AGENTS.md"

# 2. Modular Rules
link_item "$REPO_DIR/rules" "$TARGET_CONFIG_DIR/rules"

# 3. Modular Skills
link_item "$REPO_DIR/skills" "$TARGET_CONFIG_DIR/skills"

# 4. Global Hooks
link_item "$REPO_DIR/hooks/hooks.json" "$TARGET_CONFIG_DIR/hooks.json"

echo "=== Verification ==="
ls -ld "$TARGET_GEMINI_DIR/AGENTS.md"
ls -ld "$TARGET_CONFIG_DIR/rules"
ls -ld "$TARGET_CONFIG_DIR/skills"
ls -ld "$TARGET_CONFIG_DIR/hooks.json"

echo "=== Deployment Complete. Antigravity 2.0 will load these customizations across all workspaces. ==="
