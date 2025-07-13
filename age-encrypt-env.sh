#!/usr/bin/env bash
set -euo pipefail

ENV_FILE="$1"
REPO_NAME=$(basename "$(dirname "$ENV_FILE")")

ENCRYPTED_FILE="${REPO_NAME}.env.age"

if [[ ! -f "${KEY_FILE}" ]]; then
  echo "❌ Missing $KEY_FILE. Run: age-keygen -o .age-key.txt"
  exit 1
fi

if [[ ! -f "$ENV_FILE" ]]; then
  echo "❌ .env file not found: $ENV_FILE"
  exit 1
fi

PUBKEY=$(grep -o 'age1[0-9a-z]*' "${KEY_FILE}")
echo "🔐 Encrypting ${ENV_FILE}"
age -r "$PUBKEY" -o "${ENCRYPTED_FILE}" "$ENV_FILE"
echo "✅ Encrypted $ENV_FILE -> ${REPO_NAME}.env.age"
