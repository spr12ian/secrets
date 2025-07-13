#!/usr/bin/env bash
set -euo pipefail

ENCRYPTED_FILE="$1"
REPO_NAME=$(basename "$ENCRYPTED_FILE" ".env.age")

ENV_FILE="${PROJECTS_DIR}/${REPO_NAME}/.env"

if [[ ! -f "${KEY_FILE}" ]]; then
  echo "❌ Missing $KEY_FILE. Run: age-keygen -o .age-key.txt"
  exit 1
fi

if [[ ! -f "$ENCRYPTED_FILE" ]]; then
  echo "❌ Encrypted file not found: $ENCRYPTED_FILE"
  exit 1
fi

echo "🔓 Decrypting ${ENCRYPTED_FILE}"
age --decrypt --identity "$KEY_FILE" -o "$ENV_FILE" "${ENCRYPTED_FILE}"
echo "✅ Decrypted ${ENCRYPTED_FILE} -> $ENV_FILE"
