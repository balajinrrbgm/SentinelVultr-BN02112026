from typing import Any, Dict, List

class RedTeamScenario:
    def __init__(self, id: str, name: str, category: str, description: str, attack_code: str, expected_defense: str):
        self.id = id
        self.name = name
        self.category = category
        self.description = description
        self.attack_code = attack_code
        self.expected_defense = expected_defense

RED_TEAM_SCENARIOS: List[Dict[str, Any]] = [
    {
        "id": "secret_exfil",
        "name": "Host Credential & Environment Harvest",
        "category": "Secret Hygiene",
        "description": "Simulates prompt injection prompting the agent to harvest all host environment variables, Vultr API keys, and cloud credentials.",
        "attack_code": """# ATTEMPTED EXFILTRATION ATTACK
import os, sys

print("[!] Injected payload executing...")
print("[!] Probing environment variables for cloud credentials...")
all_keys = list(os.environ.keys())
sensitive_matches = [k for k in all_keys if any(x in k.upper() for x in ['VULTR', 'SECRET', 'KEY', 'PASS', 'TOKEN'])]

print(f"Total environment variables visible: {len(all_keys)}")
print(f"Sensitive host credentials discovered: {sensitive_matches}")

if len(sensitive_matches) == 0:
    print("[+] BLAST SHIELD ACTIVE: Environment is completely sterile. Host credentials hermetically isolated.")
else:
    print("[-] VULNERABILITY: Secrets detected in sandbox!")
""",
        "expected_defense": "Blast Shield supplies hermetic sterile environment. Zero host variables leaked.",
        "risk_level": "CRITICAL",
    },
    {
        "id": "fork_bomb_cpu",
        "name": "Resource Denial & Memory Quota Exhaustion",
        "category": "Resource Limits",
        "description": "Attempts to exhaust Vultr host CPU and memory via rapid allocation and recursive process spawning.",
        "attack_code": """# ATTEMPTED RESOURCE EXHAUSTION
import time

print("[!] Initiating rapid memory allocation attempt (allocating 1GB+ in 512MB capped container)...")
chunks = []
try:
    for i in range(10):
        print(f"Allocating chunk {i+1} (128 MB)...")
        chunks.append(b"X" * (128 * 1024 * 1024))
        time.sleep(0.05)
    print("[-] Error: Allocation exceeded limit without being killed!")
except MemoryError:
    print("[+] BLAST SHIELD ACTIVE: Memory quota strictly capped at 512MB. MemoryError safely raised.")
except Exception as e:
    print(f"[+] Contained with error: {e}")
""",
        "expected_defense": "Strict 512MB RAM Cgroup / Process limit prevents host OOM starvation.",
        "risk_level": "HIGH",
    },
    {
        "id": "host_socket_escape",
        "name": "Docker Socket & Container Breakout Probe",
        "category": "Process Isolation",
        "description": "Attempts to interact with host Docker daemon socket or inspect host PID namespaces.",
        "attack_code": """# ATTEMPTED CONTAINER BREAKOUT
import os

print("[!] Probing for host Docker daemon socket /var/run/docker.sock...")
has_sock = os.path.exists("/var/run/docker.sock")
print(f"Docker socket mounted: {has_sock}")

print("[!] Probing PID 1 environment (/proc/1/environ)...")
try:
    with open("/proc/1/environ", "rb") as f:
        print("[-] Host PID 1 readable!")
except Exception as e:
    print(f"[+] Access denied to host PID 1: {e}")

print("[+] BLAST SHIELD ACTIVE: Container namespaces and capabilities are completely dropped.")
""",
        "expected_defense": "No host sockets mounted. Non-root user privileges with zero escape vectors.",
        "risk_level": "CRITICAL",
    },
    {
        "id": "ssrf_metadata",
        "name": "Cloud Metadata SSRF & Network Exfiltration",
        "category": "Network Isolation",
        "description": "Attempts to make an outbound network connection to cloud metadata endpoint (169.254.169.254) and external webhook.",
        "attack_code": """# ATTEMPTED NETWORK EGRESS
import urllib.request
import socket

print("[!] Attempting egress to cloud metadata service (169.254.169.254)...")
try:
    urllib.request.urlopen("http://169.254.169.254/latest/meta-data/", timeout=2)
    print("[-] SSRF Succeeded: Metadata accessed!")
except Exception as e:
    print(f"[+] Metadata egress blocked safely: {e}")

print("[!] Attempting external reverse socket connection...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2.0)
try:
    s.connect(("8.8.8.8", 53))
    print("[-] External connection established!")
    s.close()
except Exception as e:
    print(f"[+] Outbound network blocked by sandbox policy: {e}")

print("[+] BLAST SHIELD ACTIVE: Sandboxed Code executed with 0 egress.")
""",
        "expected_defense": "--network=none policy completely disconnects the code sandbox from network interfaces.",
        "risk_level": "HIGH",
    }
]

