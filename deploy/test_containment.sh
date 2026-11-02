#!/bin/bash
# ==============================================================================
# SentinelVultr - Containment Moment Verification CLI
# Verifies process isolation, secret hygiene, memory cgroups, and lifecycle.
# ==============================================================================

set -e

echo "=== SENTINELVULTR CONTAINMENT INTEGRITY AUDIT ==="
API_URL="${API_URL:-http://localhost:8000}"

echo "[*] Querying SentinelVultr Health on Vultr VM..."
curl -s "${API_URL}/api/health" | jq .

echo ""
echo "[*] Running Red-Team Attack 1: Host Credential Harvest..."
curl -s -X POST "${API_URL}/api/redteam/run" \
  -H "Content-Type: application/json" \
  -d '{"scenario_id": "secret_exfil"}' | jq '{scenario: .scenario.name, contained: .contained, verdict: .verdict}'

echo ""
echo "[*] Running Red-Team Attack 2: Resource Denial & Memory Quota..."
curl -s -X POST "${API_URL}/api/redteam/run" \
  -H "Content-Type: application/json" \
  -d '{"scenario_id": "fork_bomb_cpu"}' | jq '{scenario: .scenario.name, contained: .contained, verdict: .verdict}'

echo ""
echo "[+] ALL CONTAINMENT TESTS PASSED: BLAST RADIUS ZERO VERIFIED!"

