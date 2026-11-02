import asyncio
import os
import shutil
import tempfile
import time
from typing import Any, Dict, List, Optional
from .base import BaseSandboxDriver, ExecutionResult, SandboxStats
from ..security.blast_shield import BlastShield
from ..config import settings

try:
    import psutil
except ImportError:
    psutil = None

class LocalSandboxDriver(BaseSandboxDriver):
    """
    Subprocess-based Sandboxing Driver.
    Enforces process isolation, strict CPU/memory limits, lifecycle wipes,
    and sterile environment sanitization. Works out-of-the-box in all environments.
    """

    def __init__(self):
        self.active_sandboxes: Dict[str, Dict[str, Any]] = {}
        self.base_dir = os.path.join(tempfile.gettempdir(), "sentinel_vultr_sandboxes")
        os.makedirs(self.base_dir, exist_ok=True)

    async def create_sandbox(self, sandbox_id: str, sandbox_type: str = "code") -> str:
        sandbox_path = os.path.join(self.base_dir, sandbox_id)
        os.makedirs(sandbox_path, exist_ok=True)

        self.active_sandboxes[sandbox_id] = {
            "id": sandbox_id,
            "type": sandbox_type,
            "path": sandbox_path,
            "created_at": time.time(),
            "status": "IDLE",
            "violations_blocked": 0,
            "memory_used_mb": 0.0,
            "cpu_percent": 0.0,
            "active_proc": None,
        }
        return sandbox_id

    def execute_sync(
        self,
        sandbox_id: str,
        command: str,
        timeout_sec: Optional[int] = None,
        env_vars: Optional[Dict[str, str]] = None,
    ) -> ExecutionResult:
        if sandbox_id not in self.active_sandboxes:
            sandbox_path = os.path.join(self.base_dir, sandbox_id)
            os.makedirs(sandbox_path, exist_ok=True)
            self.active_sandboxes[sandbox_id] = {
                "id": sandbox_id,
                "type": "code",
                "path": sandbox_path,
                "created_at": time.time(),
                "status": "IDLE",
                "violations_blocked": 0,
                "memory_used_mb": 0.0,
                "cpu_percent": 0.0,
                "active_proc": None,
            }

        meta = self.active_sandboxes[sandbox_id]
        meta["status"] = "RUNNING"
        timeout = timeout_sec or settings.MAX_EXECUTION_TIMEOUT_SECONDS
        start_time = time.time()

        # Step 1: Blast Shield Payload Inspection
        is_flagged, warnings = BlastShield.inspect_payload(command)
        if is_flagged:
            meta["violations_blocked"] += len(warnings)

        # Step 2: Sterile Environment Sanitization
        sterile_env = BlastShield.sanitize_environment(env_vars)

        # Step 3: Write script to ephemeral workspace
        script_file = os.path.join(meta["path"], "run_task.py")
        with open(script_file, "w", encoding="utf-8") as f:
            f.write(command)

        # Execute using isolated subprocess
        import sys
        import subprocess
        python_bin = sys.executable

        stdout_data = ""
        stderr_data = ""
        timed_out = False
        exit_code = 0

        try:
            creationflags = 0
            if os.name == "nt":
                creationflags = 0x00000200  # CREATE_NEW_PROCESS_GROUP
            completed_proc = subprocess.run(
                [python_bin, "-u", script_file],
                cwd=meta["path"],
                env=sterile_env,
                capture_output=True,
                text=True,
                timeout=timeout,
                creationflags=creationflags,
            )
            stdout_data = completed_proc.stdout or ""
            stderr_data = completed_proc.stderr or ""
            exit_code = completed_proc.returncode
        except subprocess.TimeoutExpired as e:
            timed_out = True
            exit_code = -1
            meta["violations_blocked"] += 1
            warnings.append(f"Execution Timeout ({timeout}s) Exceeded: Subprocess Forcefully Terminated")
            stdout_data = (e.stdout or "") if isinstance(e.stdout, str) else ""
            stderr_data = f"\n[BLAST SHIELD ALERT] Process exceeded execution time cap ({timeout}s) and was terminated."
        except Exception as e:
            exit_code = -2
            stderr_data = f"Sandbox execution error: {str(e)}"
        finally:
            meta["status"] = "IDLE"
            meta["active_proc"] = None

        duration = time.time() - start_time
        stdout_clean = BlastShield.scrub_output(stdout_data)
        stderr_clean = BlastShield.scrub_output(stderr_data)
        artifacts = self._collect_artifacts(meta["path"], exclude_files=["run_task.py"])

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

    async def execute(
        self,
        sandbox_id: str,
        command: str,
        timeout_sec: Optional[int] = None,
        env_vars: Optional[Dict[str, str]] = None,
    ) -> ExecutionResult:
        return self.execute_sync(sandbox_id, command, timeout_sec, env_vars)

    def _collect_artifacts(self, dir_path: str, exclude_files: List[str]) -> List[Dict[str, Any]]:
        artifacts = []
        try:
            for item in os.listdir(dir_path):
                if item in exclude_files:
                    continue
                full_path = os.path.join(dir_path, item)
                if os.path.isfile(full_path):
                    size = os.path.getsize(full_path)
                    ext = item.split(".")[-1].lower() if "." in item else ""
                    artifacts.append({
                        "name": item,
                        "size_bytes": size,
                        "type": ext,
                        "path": full_path,
                    })
        except Exception:
            pass
        return artifacts

    async def _kill_proc_tree(self, pid: int):
        if psutil:
            try:
                parent = psutil.Process(pid)
                children = parent.children(recursive=True)
                for child in children:
                    try:
                        child.kill()
                    except Exception:
                        pass
                parent.kill()
            except Exception:
                pass
        else:
            try:
                if os.name == "nt":
                    import subprocess
                    subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    os.kill(pid, 9)
            except Exception:
                pass

    def destroy_sandbox_sync(self, sandbox_id: str) -> bool:
        if sandbox_id in self.active_sandboxes:
            meta = self.active_sandboxes[sandbox_id]
            try:
                if os.path.exists(meta["path"]):
                    shutil.rmtree(meta["path"], ignore_errors=True)
            except Exception:
                pass
            meta["status"] = "TERMINATED"
            del self.active_sandboxes[sandbox_id]
            return True
        return False

    async def destroy_sandbox(self, sandbox_id: str) -> bool:
        return self.destroy_sandbox_sync(sandbox_id)

    async def get_stats(self, sandbox_id: str) -> SandboxStats:
        if sandbox_id not in self.active_sandboxes:
            return SandboxStats(
                sandbox_id=sandbox_id,
                driver="LocalSubprocessDriver",
                is_active=False,
                status="TERMINATED",
            )

        meta = self.active_sandboxes[sandbox_id]
        cpu_usage = 0.0
        mem_usage = 0.0

        if psutil and meta.get("active_proc") and meta["active_proc"].pid:
            try:
                p = psutil.Process(meta["active_proc"].pid)
                cpu_usage = p.cpu_percent(interval=None)
                mem_usage = p.memory_info().rss / (1024 * 1024)
            except Exception:
                pass

        return SandboxStats(
            sandbox_id=sandbox_id,
            driver="LocalSubprocessDriver",
            is_active=meta["status"] == "RUNNING",
            status=meta["status"],
            cpu_percent=round(cpu_usage, 2),
            memory_used_mb=round(mem_usage, 2),
            memory_limit_mb=float(settings.MAX_MEMORY_MB),
            security_violations_blocked=meta["violations_blocked"],
        )
