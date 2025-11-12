#!/usr/bin/env bash
set -euo pipefail
EXECUTE="${1:-}"

NAMES=(
  "**[APP]**/dev/backend/DB_URL"
  "**[APP]**/dev/backend/JWT_SECRET"
  "**[APP]**/dev/ci/GITHUB_APP_PRIVATE_KEY"
  "**[APP]**/dev/registry/ECR_PASSWORD"
)

echo "Secrets to ensure (dev):"
for n in "${NAMES[@]}"; do echo " - $n"; done

if [[ "$EXECUTE" != "--execute" ]]; then
  echo -e "\nDRY-RUN: pass --execute to create empty secrets ({})."
  exit 0
fi

for n in "${NAMES[@]}"; do
  if aws secretsmanager describe-secret --secret-id "$n" >/dev/null 2>&1; then
    echo "Exists: $n"
    continue
  fi
  echo "Creating: $n"
  aws secretsmanager create-secret --name "$n" \
    --secret-string '{}' \
    --tags Key=created_by,Value=orchestrator Key=env,Value=dev
done
echo "Done."
