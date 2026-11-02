import time
import logging
from typing import Any, Dict, List, Optional
from .base import ExecutionResult
from .docker_driver import DockerSandboxDriver
from ..vultr_inference import vultr_client

logger = logging.getLogger("sentinel.code")

class CodeExecutor:
    """
    Pattern A: Sandboxed Code Execution Engine.
    Executes code in isolated Vultr sandboxes with self-healing feedback loops.
    """

    def __init__(self, driver: Optional[DockerSandboxDriver] = None):
        self.driver = driver or DockerSandboxDriver()

    async def run_with_self_healing(
        self,
        sandbox_id: str,
        initial_code: str,
        task_description: str,
        max_retries: int = 2,
    ) -> Dict[str, Any]:
        """
        Executes code inside the sandbox. If execution fails (exit_code != 0),
        feeds stdout/stderr back to Vultr Serverless Inference for a self-healing retry.
        """
        attempts: List[Dict[str, Any]] = []
        current_code = initial_code

        for attempt_idx in range(max_retries + 1):
            start_t = time.time()
            result: ExecutionResult = await self.driver.execute(sandbox_id, current_code)
            duration = time.time() - start_t

            attempts.append({
                "attempt": attempt_idx + 1,
                "code": current_code,
                "exit_code": result.exit_code,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "duration_sec": result.duration_sec,
                "timed_out": result.timed_out,
                "containment_alerts": result.containment_alerts,
                "artifacts": result.artifacts,
            })

            if result.exit_code == 0:
                # Success!
                return {
                    "success": True,
                    "final_attempt": attempt_idx + 1,
                    "history": attempts,
                    "final_output": result.stdout,
                    "artifacts": result.artifacts,
                    "containment_alerts": result.containment_alerts,
                }

            # If failed and retries left, ask Vultr model to repair code
            if attempt_idx < max_retries:
                logger.info(f"Execution failed on attempt {attempt_idx+1}. Triggering self-healing repair via Vultr...")
                repair_prompt = [
                    {
                        "role": "system",
                        "content": "You are an automated code repair specialist. The sandboxed Python code failed with errors. Return ONLY the corrected, executable Python code with no markdown formatting or commentary."
                    },
                    {
                        "role": "user",
                        "content": f"Task: {task_description}\n\nFailing Code:\n{current_code}\n\nStderr / Error:\n{result.stderr}\n\nStdout:\n{result.stdout}\n\nPlease repair the code so it executes successfully."
                    }
                ]
                resp = await vultr_client.chat_completion(repair_prompt, temperature=0.1)
                repaired_content = resp["choices"][0]["message"]["content"]
                # Clean any markdown code blocks
                if "```python" in repaired_content:
                    current_code = repaired_content.split("```python")[1].split("```")[0].strip()
                elif "```" in repaired_content:
                    current_code = repaired_content.split("```")[1].split("```")[0].strip()
                else:
                    current_code = repaired_content.strip()

        # Exhausted retries
        return {
            "success": False,
            "final_attempt": max_retries + 1,
            "history": attempts,
            "final_output": attempts[-1]["stderr"] or attempts[-1]["stdout"],
            "artifacts": attempts[-1]["artifacts"],
            "containment_alerts": attempts[-1]["containment_alerts"],
        }

