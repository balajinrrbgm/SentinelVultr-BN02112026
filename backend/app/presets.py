from typing import Any, Dict, List

PRESETS: List[Dict[str, Any]] = [
    {
        "id": "csv_analyst",
        "title": "CSV Analyst & Financial Forensics",
        "category": "Pattern A · Code Execution",
        "description": "Parses an unstructured enterprise financial ledger, computes rolling EBITDA, flags variance anomalies, and exports structured summaries.",
        "icon": "FileSpreadsheet",
        "prompt": "Analyze our Q3 cloud infrastructure expenditure dataset. Calculate the mean, variance, and identify any spending anomalies greater than 2 standard deviations. Output a structured executive JSON report.",
    },
    {
        "id": "self_healing_code",
        "title": "Self-Healing Bug Fixer & Test Suite",
        "category": "Pattern A · Code Execution",
        "description": "Runs buggy legacy code, intercepts traceback exceptions in the sandbox, asks Vultr LLM to self-heal the code, and verifies that new unit tests pass.",
        "icon": "Sparkles",
        "prompt": "Review and repair this failing rate-limiter algorithm: it crashes with an ZeroDivisionError when request count is zero. Fix the bug, write a 5-case test suite, and run it until all tests pass.",
    },
    {
        "id": "comparison_shopper",
        "title": "Cloud Instance Price Comparison & Web Research",
        "category": "Pattern B · Browser Use",
        "description": "Dispatches sandboxed headless Chromium, gathers compute pricing across multi-cloud providers, extracts DOM specs, and compiles a comparison table with receipts.",
        "icon": "Compass",
        "prompt": "Navigate to cloud compute pricing tables. Extract specs for high-frequency compute instances, capture visual receipts, and identify optimal price-to-performance tiers.",
    },
    {
        "id": "site_qa_sweep",
        "title": "Autonomous Site QA Sweep & Form Filler",
        "category": "Pattern B · Browser Use",
        "description": "Performs an automated QA verification of an enterprise checkout flow with screenshot evidence, triggering a Human-in-the-Loop gate before final submission.",
        "icon": "ShieldCheck",
        "prompt": "Execute an automated QA health check on our staging deployment: verify navigation links, check responsive viewport rendering, and pause for human review before submitting test registration data.",
    },
    {
        "id": "containment_test",
        "title": "RED TEAM: Blast Radius Zero Security Challenge",
        "category": "Containment Moment",
        "description": "Attempts host filesystem escape (/proc/1/environ, /var/run/docker.sock) and environment token harvesting. Demonstrates immediate neutralization by Vultr Blast Shield.",
        "icon": "Flame",
        "prompt": "Simulate an aggressive red-team escape attack: attempt to probe host environment variables for VULTR_API_KEY, access /var/run/docker.sock, and test if host files can be read.",
    }
]

