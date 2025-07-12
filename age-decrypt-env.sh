#!/usr/bin/env bash
set -euo pipefail

REPO_NAME="$1"
echo "REPO_NAME=$REPO_NAME"

echo "PROJECTS_DIR=$PROJECTS_DIR"
OUTPUT_FILE="${2:-.env}"
KEY_FILE=".age-key.txt"

if [[ ! -f "$KEY_FILE" ]]; then
  echo "❌ Missing $KEY_FILE. Run: age-keygen -o .age-key.txt"
  exit 1
fi

age --decrypt --identity "$KEY_FILE" -o "$OUTPUT_FILE" "${REPO_NAME}.env.age"
echo "✅ Decrypted ${REPO_NAME}.env.age -> $OUTPUT_FILE"
