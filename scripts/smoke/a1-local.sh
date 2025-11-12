#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
echo "ok $(date -u)" > scripts/smoke/_smoke_write_test.txt
test -f scripts/smoke/_smoke_write_test.txt
echo "SMOKE PASS"
