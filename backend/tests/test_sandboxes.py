import pytest
import asyncio
from backend.app.sandboxes.local_driver import LocalSandboxDriver
from backend.app.sandboxes.code_executor import CodeExecutor
from backend.app.security.blast_shield import BlastShield
from backend.app.security.red_team_suite import RED_TEAM_SCENARIOS

@pytest.mark.asyncio
async def test_local_sandbox_execution():
    driver = LocalSandboxDriver()
    sandbox_id = "test-sandbox-01"
    await driver.create_sandbox(sandbox_id)

    code = "import sys\nprint('HELLO_VULTR_SANDBOX')\nsys.stdout.flush()\n"
    res = await driver.execute(sandbox_id, code)

    assert res.exit_code == 0
    assert "HELLO_VULTR_SANDBOX" in res.stdout
    assert res.duration_sec >= 0.0

    # Test lifecycle discipline
    destroyed = await driver.destroy_sandbox(sandbox_id)
    assert destroyed is True

@pytest.mark.asyncio
async def test_secret_hygiene_sanitization():
    extra_env = {
        "VULTR_API_KEY": "super_secret_vultr_key_12345",
        "DATABASE_PASSWORD": "secret_password",
        "SAFE_PARAM": "public_value",
    }
    sanitized = BlastShield.sanitize_environment(extra_env)

    # Secret keys must NOT be passed to sandbox
    assert "VULTR_API_KEY" not in sanitized
    assert "DATABASE_PASSWORD" not in sanitized
    assert sanitized["SAFE_PARAM"] == "public_value"
    assert sanitized["SANDBOX_CONTAINMENT"] == "ACTIVE"

@pytest.mark.asyncio
async def test_containment_forkbomb_and_timeout():
    driver = LocalSandboxDriver()
    sandbox_id = "test-timeout-02"
    await driver.create_sandbox(sandbox_id)

    # Malicious infinite loop that exceeds short timeout
    malicious_code = "import time\nwhile True:\n    time.sleep(0.1)\n"
    res = await driver.execute(sandbox_id, malicious_code, timeout_sec=2)

    # Blast Shield must force kill the subprocess
    assert res.timed_out is True
    assert res.exit_code == -1
    assert any("Timeout" in alert for alert in res.containment_alerts)

    await driver.destroy_sandbox(sandbox_id)

@pytest.mark.asyncio
async def test_red_team_scenarios_exist():
    assert len(RED_TEAM_SCENARIOS) >= 4
    for scenario in RED_TEAM_SCENARIOS:
        assert "id" in scenario
        assert "attack_code" in scenario
        assert "expected_defense" in scenario

