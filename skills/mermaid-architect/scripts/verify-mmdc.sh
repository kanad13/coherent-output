#!/usr/bin/env bash
# Verifies a Mermaid (.mmd) file by testing headless SVG compilation via npx @mermaid-js/mermaid-cli
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <path-to-mermaid-file.mmd>"
  exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="$(mktemp).svg"

if ! command -v npx &> /dev/null; then
  echo "Warning: npx not installed. Skipping headless mmdc compilation check."
  exit 0
fi

echo "Verifying Mermaid syntax for: $INPUT_FILE"
if npx -y @mermaid-js/mermaid-cli -i "$INPUT_FILE" -o "$OUTPUT_FILE" -e svg --quiet 2>/dev/null; then
  echo "Success: Mermaid diagram compiled cleanly."
  rm -f "$OUTPUT_FILE"
  exit 0
else
  echo "Error: Mermaid syntax validation failed."
  rm -f "$OUTPUT_FILE"
  exit 1
fi
