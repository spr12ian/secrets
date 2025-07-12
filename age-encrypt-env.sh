#!/usr/bin/env bash
set -euo pipefail

echo "\$PROJECTS_DIR=${PROJECTS_DIR}"
REPO_NAME="$1"
ENV_FILE="$2"
PUBKEY=$(grep -o 'age1[0-9a-z]*' .age-key.txt)

if [[ ! -f "$ENV_FILE" ]]; then
  echo "❌ .env file not found at $ENV_FILE"
  exit 1
fi

age -r "$PUBKEY" -o "${REPO_NAME}.env.age" "$ENV_FILE"
echo "✅ Encrypted $ENV_FILE -> ${REPO_NAME}.env.age"
