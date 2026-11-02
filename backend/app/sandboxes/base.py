from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

try:
    from pydantic import BaseModel
except ImportError:
    class BaseModel:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        def model_dump(self):
            return self.__dict__

class SandboxStats(BaseModel):
    sandbox_id: str
    driver: str
    is_active: bool
    cpu_percent: float = 0.0
    memory_used_mb: float = 0.0
    memory_limit_mb: float = 512.0
    network_egress_bytes: int = 0
    security_violations_blocked: int = 0
    status: str = "IDLE"  # "IDLE", "RUNNING", "TERMINATED", "QUARANTINED"

class ExecutionResult(BaseModel):
    sandbox_id: str
    exit_code: int
    stdout: str
    stderr: str
    duration_sec: float
    timed_out: bool = False
    containment_alerts: List[str] = []
    artifacts: List[Dict[str, Any]] = []

class BaseSandboxDriver(ABC):
    @abstractmethod
    async def create_sandbox(self, sandbox_id: str, sandbox_type: str = "code") -> str:
        """Create and initialize an isolated sandbox environment."""
        pass

    @abstractmethod
    async def execute(
        self,
        sandbox_id: str,
        command: str,
        timeout_sec: Optional[int] = None,
        env_vars: Optional[Dict[str, str]] = None,
    ) -> ExecutionResult:
        """Execute a payload inside the isolated sandbox."""
        pass

    @abstractmethod
    async def destroy_sandbox(self, sandbox_id: str) -> bool:
        """Clean up and wipe all state associated with the sandbox."""
        pass

    @abstractmethod
    async def get_stats(self, sandbox_id: str) -> SandboxStats:
        """Query real-time resource and telemetry stats."""
        pass
