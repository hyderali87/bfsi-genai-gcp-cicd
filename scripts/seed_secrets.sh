#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID="${1:?Usage: ./scripts/seed_secrets.sh <PROJECT_ID> <API_KEY>}"
API_KEY="${2:?Usage: ./scripts/seed_secrets.sh <PROJECT_ID> <API_KEY>}"

echo -n "${API_KEY}" | gcloud secrets versions add bfsi-api-key --project="${PROJECT_ID}" --data-file=-
echo "Seeded bfsi-api-key"
