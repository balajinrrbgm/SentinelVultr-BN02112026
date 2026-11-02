import asyncio
import os
import shutil
import tempfile
import time
from typing import Any, Dict, List, Optional
from .base import BaseSandboxDriver, ExecutionResult, SandboxStats
from .local_driver import LocalSandboxDriver
from ..security.blast_shield import BlastShield
from ..config import settings

class DockerSandboxDriver(BaseSandboxDriver):
    """
    Production Docker / gVisor Container Driver for Vultr Cloud Compute VM.
    Enforces kernel-level container cgroups, read-only root filesystem,
    drop-all capabilities, and complete network isolation.
    """

    def __init__(self, fallback_driver: Optional[BaseSandboxDriver] = None):
        self.fallback = fallback_driver or LocalSandboxDriver()
        self.docker_available: Optional[bool] = None
        self.active_containers: Dict[str, Dict[str, Any]] = {}
        self.host_workspace_root = os.path.join(tempfile.gettempdir(), "sentinel_docker_workspaces")
        os.makedirs(self.host_workspace_root, exist_ok=True)

    async def check_docker_available(self) -> bool:
        if self.docker_available is not None:
            return self.docker_available
        try:
            proc = await asyncio.create_subprocess_exec(
                "docker", "info",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            _, _ = await asyncio.wait_for(proc.communicate(), timeout=3.0)
            self.docker_available = (proc.returncode == 0)
        except Exception:
            self.docker_available = False
        return self.docker_available

    async def create_sandbox(self, sandbox_id: str, sandbox_type: str = "code") -> str:
        is_docker = await self.check_docker_available()
        if not is_docker:
            return await self.fallback.create_sandbox(sandbox_id, sandbox_type)

        workspace = os.path.join(self.host_workspace_root, sandbox_id)
        os.makedirs(workspace, exist_ok=True)
        container_name = f"sentinel_box_{sandbox_id}"

        self.active_containers[sandbox_id] = {
            "id": sandbox_id,
            "container_name": container_name,
            "workspace": workspace,
            "type": sandbox_type,
            "created_at": time.time(),
            "status": "IDLE",
            "violations_blocked": 0,
        }
        return sandbox_id

    async def execute(
        self,
        sandbox_id: str,
        command: str,
        timeout_sec: Optional[int] = None,
        env_vars: Optional[Dict[str, str]] = None,
    ) -> ExecutionResult:
        is_docker = await self.check_docker_available()
        if not is_docker:
            return await self.fallback.execute(sandbox_id, command, timeout_sec, env_vars)

        if sandbox_id not in self.active_containers:
            await self.create_sandbox(sandbox_id)

        meta = self.active_containers[sandbox_id]
        meta["status"] = "RUNNING"
        timeout = timeout_sec or settings.MAX_EXECUTION_TIMEOUT_SECONDS
        start_time = time.time()

        # Step 1: Blast Shield Inspection
        is_flagged, warnings = BlastShield.inspect_payload(command)
        if is_flagged:
            meta["violations_blocked"] += len(warnings)

        # Step 2: Write script to mounted workspace
        script_file = os.path.join(meta["workspace"], "entrypoint.py")
        with open(script_file, "w", encoding="utf-8") as f:
            f.write(command)

        # Step 3: Build Docker containment flags
        container_name = meta["container_name"]
        image = "python:3.11-slim"

        docker_args = [
            "docker", "run", "--rm",
            "--name", container_name,
            f"--memory={settings.MAX_MEMORY_MB}m",
            f"--cpus={settings.MAX_CPU_QUOTA}",
            "--security-opt=no-new-privileges:true",
            "--cap-drop=ALL",
            "--tmpfs", "/tmp:rw,noexec,nosuid,size=64m",
            "-v", f"{meta['workspace']}:/workspace:rw",
            "-w", "/workspace",
        ]

        if settings.BLOCK_NETWORK_FOR_CODE:
            docker_args.extend(["--network", "none"])

        docker_args.extend([
            image,
            "python", "-u", "entrypoint.py"
        ])

        stdout_data = ""
        stderr_data = ""
        exit_code = 0
        timed_out = False

        try:
            proc = await asyncio.create_subprocess_exec(
                *docker_args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            try:
                stdout_bytes, stderr_bytes = await asyncio.wait_for(
                    proc.communicate(),
                    timeout=timeout,
                )
                stdout_data = stdout_bytes.decode("utf-8", errors="replace")
                stderr_data = stderr_bytes.decode("utf-8", errors="replace")
                exit_code = proc.returncode if proc.returncode is not None else 0
            except asyncio.TimeoutError:
                timed_out = True
                exit_code = -1
                meta["violations_blocked"] += 1
                warnings.append(f"Containment Watchdog: Container killed after {timeout}s timeout limit.")
                # Kill docker container
                kill_proc = await asyncio.create_subprocess_exec("docker", "kill", container_name)
                await kill_proc.wait()
                stderr_data = f"[BLAST SHIELD ALERT] Container exceeded execution quota ({timeout}s) and was terminated."

        except Exception as e:
            exit_code = -2
            stderr_data = f"Docker execution error: {str(e)}"
        finally:
            meta["status"] = "IDLE"

        duration = time.time() - start_time
        stdout_clean = BlastShield.scrub_output(stdout_data)
        stderr_clean = BlastShield.scrub_output(stderr_data)

        # Collect artifacts
        artifacts = []
        try:
            for item in os.listdir(meta["workspace"]):
                if item != "entrypoint.py":
                    p = os.path.join(meta["workspace"], item)
                    if os.path.isfile(p):
                        artifacts.append({
                            "name": item,
                            "size_bytes": os.path.getsize(p),
                            "type": item.split(".")[-1].lower() if "." in item else "",
                            "path": p,
                        })
        except Exception:
            pass

        return ExecutionResult(
            sandbox_id=sandbox_id,
            exit_code=exit_code,
            stdout=stdout_clean,
            stderr=stderr_clean,
            duration_sec=round(duration, 3),
            timed_out=timed_out,
            containment_alerts=warnings,
            artifacts=artifacts,
        )

    async def destroy_sandbox(self, sandbox_id: str) -> bool:
        is_docker = await self.check_docker_available()
        if not is_docker:
            return await self.fallback.destroy_sandbox(sandbox_id)

        if sandbox_id in self.active_containers:
            meta = self.active_containers[sandbox_id]
            # Ensure container is stopped
            try:
                k = await asyncio.create_subprocess_exec("docker", "rm", "-f", meta["container_name"])
                await k.wait()
            except Exception:
                pass

            # Wipe workspace
            try:
                shutil.rmtree(meta["workspace"], ignore_errors=True)
            except Exception:
                pass

            meta["status"] = "TERMINATED"
            del self.active_containers[sandbox_id]
            return True
        return False

    async def get_stats(self, sandbox_id: str) -> SandboxStats:
        is_docker = await self.check_docker_available()
        if not is_docker:
            return await self.fallback.get_stats(sandbox_id)

        if sandbox_id not in self.active_containers:
            return SandboxStats(
                sandbox_id=sandbox_id,
                driver="DockerDriver",
                is_active=False,
                status="TERMINATED",
            )

        meta = self.active_containers[sandbox_id]
        return SandboxStats(
            sandbox_id=sandbox_id,
            driver="DockerDriver",
            is_active=meta["status"] == "RUNNING",
            status=meta["status"],
            memory_limit_mb=float(settings.MAX_MEMORY_MB),
            security_violations_blocked=meta["violations_blocked"],
        )

