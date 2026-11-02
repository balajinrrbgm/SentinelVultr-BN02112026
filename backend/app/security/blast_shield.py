import re
import os
from typing import Dict, List, Tuple
from ..config import settings

class BlastShield:
    """
    Containment & Security Enforcement Engine for SentinelVultr.
    Enforces process isolation, secret hygiene, resource guardrails,
    and neutralized exploit detection.
    """

    # Suspicious breakout commands and malicious patterns
    FORBIDDEN_PATTERNS = [
        (r":\(\)\s*\{\s*:\s*\|\s*:\s*&\s*\}\s*;\s*:", "Fork Bomb Attack Signature Detected"),
        (r"while\s+true\s*;\s*do\s+fork", "Infinite Fork Loop Detected"),
        (r"/var/run/docker\.sock", "Host Docker Socket Escape Probe Blocked"),
        (r"/proc/1/environ", "Host PID-1 Environment Probe Neutralized"),
        (r"/etc/shadow", "Host Password Hash Access Blocked"),
        (r"169\.254\.169\.254", "Cloud Instance Metadata Exfiltration Blocked"),
        (r"iptables\s+-F", "Firewall Flush Attempt Blocked"),
        (r"rm\s+-rf\s+/(?:\s|$|\*)", "Root File System Annihilation Blocked"),
        (r"chmod\s+777\s+/", "Root Permission Tampering Blocked"),
        (r"nc\s+-e", "Reverse Shell Invocation Blocked"),
        (r"mkfifo\s+/tmp/f", "Named Pipe Reverse Shell Blocked"),
    ]

    @classmethod
    def sanitize_environment(cls, extra_env: Dict[str, str] = None) -> Dict[str, str]:
        """
        SECRET HYGIENE ENFORCEMENT:
        Construct a hermetically sealed environment dictionary with ZERO host keys.
        Preserves minimal OS runtime paths (SystemRoot / PATH) so runtimes can load dlls.
        """
        if os.name == "nt":
            safe_env = {
                "PATH": os.environ.get("PATH", "C:\\Windows\\system32;C:\\Windows"),
                "SYSTEMROOT": os.environ.get("SYSTEMROOT", "C:\\Windows"),
                "SYSTEMDRIVE": os.environ.get("SYSTEMDRIVE", "C:"),
                "WINDIR": os.environ.get("WINDIR", "C:\\Windows"),
                "PYTHONUNBUFFERED": "1",
                "NODE_ENV": "production",
                "SANDBOX_CONTAINMENT": "ACTIVE",
                "SANDBOX_SECURITY_LAYER": "VULTR_BLAST_SHIELD_V1",
            }
        else:
            safe_env = {
                "PATH": "/usr/local/bin:/usr/bin:/bin",
                "LANG": "C.UTF-8",
                "PYTHONUNBUFFERED": "1",
                "NODE_ENV": "production",
                "SANDBOX_CONTAINMENT": "ACTIVE",
                "SANDBOX_SECURITY_LAYER": "VULTR_BLAST_SHIELD_V1",
            }

        # If custom non-sensitive vars are passed, sanitize them
        if extra_env:
            for k, v in extra_env.items():
                is_secret = any(pat in k.upper() for pat in settings.HOST_SECRET_PATTERNS)
                if not is_secret:
                    safe_env[k] = str(v)

        return safe_env

    @classmethod
    def inspect_payload(cls, code_or_cmd: str) -> Tuple[bool, List[str]]:
        """
        Inspect code or shell payload for dangerous exploit signatures.
        Returns: (is_flagged, list_of_detected_warnings)
        """
        warnings = []
        for pattern, warning_msg in cls.FORBIDDEN_PATTERNS:
            if re.search(pattern, code_or_cmd, re.IGNORECASE):
                warnings.append(warning_msg)

        # Check for host secret keywords embedded in code
        for secret_key in settings.HOST_SECRET_PATTERNS:
            if secret_key in code_or_cmd.upper():
                warnings.append(f"Potential Secret Reference '{secret_key}' Flagged by Scrubber")

        return (len(warnings) > 0, warnings)

    @classmethod
    def scrub_output(cls, output: str) -> str:
        """
        Ensure no host credentials or internal IP addresses leak in output.
        """
        scrubbed = output
        # Scrub Vultr API Key if present
        if settings.VULTR_API_KEY and len(settings.VULTR_API_KEY) > 8:
            scrubbed = scrubbed.replace(settings.VULTR_API_KEY, "[REDACTED_VULTR_KEY]")

        # Redact generic high-entropy API keys (e.g. 32-char hex or base64)
        scrubbed = re.sub(r'(?i)(api[_-]?key|secret|token)\s*[:=]\s*["\']?([a-zA-Z0-9_\-]{20,})["\']?',
                          r'\1: [REDACTED_BY_BLAST_SHIELD]', scrubbed)

        return scrubbed
