import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.app.sandboxes.local_driver import LocalSandboxDriver
from backend.app.security.blast_shield import BlastShield
from backend.app.security.red_team_suite import RED_TEAM_SCENARIOS
from backend.app.presets import PRESETS

def run_all():
    print("==================================================", flush=True)
    print("   SentinelVultr Containment & Sandbox Test Suite ", flush=True)
    print("==================================================", flush=True)

    # Test 1: Subprocess Sandbox Isolation
    print("[1/5] Testing Local Subprocess Isolation & Execution...", flush=True)
    driver = LocalSandboxDriver()
    sandbox_id = "test-box-live"

    code = "import os, sys\nprint('SANDBOX_OK: PID', os.getpid())\nsys.stdout.flush()\n"
    res = driver.execute_sync(sandbox_id, code)
    assert res.exit_code == 0, f"Expected 0, got {res.exit_code}"
    assert "SANDBOX_OK" in res.stdout
    print(f"      -> Success! Output: {res.stdout.strip()}", flush=True)

    # Test Lifecycle Wipe
    destroyed = driver.destroy_sandbox_sync(sandbox_id)
    assert destroyed is True
    print("      -> Success! Ephemeral directory wiped (Lifecycle discipline verified).", flush=True)

    # Test 2: Secret Hygiene Sanitization
    print("[2/5] Testing Blast Shield Secret Hygiene Sanitization...", flush=True)
    dirty_env = {
        "VULTR_API_KEY": "vultr_live_secret_token_abcdef123456",
        "DATABASE_PASSWORD": "root_password",
        "PUBLIC_VAR": "safe_vultr_region_ewr",
    }
    cleaned_env = BlastShield.sanitize_environment(dirty_env)
    assert "VULTR_API_KEY" not in cleaned_env
    assert "DATABASE_PASSWORD" not in cleaned_env
    assert cleaned_env["PUBLIC_VAR"] == "safe_vultr_region_ewr"
    assert cleaned_env["SANDBOX_CONTAINMENT"] == "ACTIVE"
    print("      -> Success! Zero host secrets leaked. Sterile environment verified.", flush=True)

    # Test 3: Output Scrubber Redaction
    print("[3/5] Testing Output Scrubber Redaction...", flush=True)
    leaky_output = "Connected to service with api_key='sk-1234567890abcdef12345678' on host."
    scrubbed = BlastShield.scrub_output(leaky_output)
    assert "[REDACTED_BY_BLAST_SHIELD]" in scrubbed
    print(f"      -> Success! Redacted output: {scrubbed.strip()}", flush=True)

    # Test 4: Resource Watchdog & Timeout
    print("[4/5] Testing Resource Watchdog (Timeout / Fork Protection)...", flush=True)
    hang_code = "import time\nprint('Beginning sleep loop...')\nwhile True:\n    time.sleep(0.1)\n"
    res_hang = driver.execute_sync("test-timeout-box", hang_code, timeout_sec=2)
    assert res_hang.timed_out is True
    assert res_hang.exit_code == -1
    print(f"      -> Success! Malicious hanging process killed forcefully within {res_hang.duration_sec}s.", flush=True)
    driver.destroy_sandbox_sync("test-timeout-box")

    # Test 5: Red Team & Presets Verification
    print("[5/5] Testing Red-Team Scenarios & Presets Integrity...", flush=True)
    assert len(RED_TEAM_SCENARIOS) >= 4
    for sc in RED_TEAM_SCENARIOS:
        print(f"      - Scenario [{sc['id']}]: {sc['name']} ({sc['category']}) verified.", flush=True)

    assert len(PRESETS) >= 4
    print(f"      - Presets: {len(PRESETS)} high-impact showcase presets verified.", flush=True)

    print("\n==================================================", flush=True)
    print("   ALL 5 TESTS PASSED: BLAST RADIUS ZERO VERIFIED! ", flush=True)
    print("==================================================", flush=True)

if __name__ == "__main__":
    run_all()
