# LabLab.ai Hackathon Submission Package
## Vultr: Agent Rush Hackathon · Challenge 01: Blast Radius Zero

---

## 📋 Basic Information

### Project Title
**SentinelVultr · Zero-Radius Sandboxed Autonomous Agent Platform**

### Short Description (1-2 sentences)
A production-grade autonomous agent control plane that plans, dispatches, and verifies real code and browser actions inside ephemeral, isolated Vultr sandboxes — zero blast radius, zero host leaks, and 100% verified execution.

### Category
**Challenge 01 · Blast Radius Zero** (Sandboxed Code Execution, Browser Automation & Containment Security)

### Technology & Category Tags
`Vultr Cloud Compute`, `Vultr Serverless Inference`, `Docker`, `gVisor`, `Playwright`, `Python`, `FastAPI`, `Next.js`, `Autonomous Agents`, `Sandboxing`, `DevSecOps`, `Llama-3.3`

---

## 📝 Long Description

### The Problem
Autonomous AI agents possess extraordinary potential to write code, conduct research, and automate operations. However, enterprises refuse to deploy autonomous agents into real-world production environments due to the **"Blast Radius"**:
1. **Rogue Execution & Breakouts:** An agent could delete files, tamper with permissions, or compromise the host server.
2. **Secret Harvesting & Exfiltration:** Injected prompts can coerce agents into scraping host environment variables, cloud API keys, and credentials.
3. **Resource Starvation:** Uncontrolled loops or fork bombs can exhaust CPU and RAM, taking down mission-critical host infrastructure.
4. **Lack of Verifiable Output:** Chatbots merely describe what they would do; enterprise workflows require verifiable artifacts.

### The Solution: SentinelVultr
**SentinelVultr** acts as a centralized control layer hosted on **Vultr Cloud Compute**, dispatching real work into isolated execution environments and returning verifiable output:

- **Dual-Engine Sandboxing**:
  - **Pattern A (Code Execution):** Ingests raw analytical goals, synthesizes executable Python code, runs it in an isolated container with zero outbound network access, and leverages a self-healing retry loop via Vultr Serverless Inference.
  - **Pattern B (Browser Use):** Launches sandboxed headless Chromium via Playwright, streams DOM and screenshot proofs to the user, and gates sensitive actions behind Human-in-the-Loop authorization.
- **The Blast Shield (Hardware-Enforced Containment):**
  - **Process Isolation:** Drop-all Linux capabilities (`--cap-drop=ALL`), non-root UID execution, and namespace isolation.
  - **Secret Hygiene:** Hermetically sealed execution environments with zero host keys or Vultr API credentials.
  - **Resource Caps:** Hard cgroup limits of 512MB RAM and 1.0 vCPU with watchdog timeouts.
  - **Lifecycle Discipline:** Complete ephemeral destruction and disk wipe upon task completion.
- **Vultr Serverless Inference Engine:**
  - Direct integration with `https://api.vultrinference.com/v1` for low-latency planning, code synthesis, and closed-loop self-healing with `meta-llama/llama-3.3-70b-instruct`.

---

## 🎥 Demo Video Script (2-3 Minutes)
*Demonstrates multi-step agentic workflows and the required Containment Moment.*

| Time | Scene | Visual / Screen Action | Voiceover Script |
| :--- | :--- | :--- | :--- |
| **0:00 - 0:25** | The Hook & Problem | Show SentinelVultr Dashboard on Vultr VM. Highlight the Blast Shield status. | *"An agent that only chats is a demo; an agent that executes safely is a product. Welcome to SentinelVultr, the zero-radius autonomous agent platform running on Vultr Cloud Compute."* |
| **0:25 - 0:55** | Pattern A: Sandboxed Code Execution | Select 'CSV Analyst' preset. Click 'Dispatch Mission'. | *"Watch as our agent takes an unstructured financial dataset. Powered by Vultr Serverless Inference running Llama 3.3, it decomposes the mission, provisions an ephemeral container with a 512MB RAM cap and zero network access, executes statistical variance calculations, and returns verifiable output."* |
| **0:55 - 1:25** | Pattern B: Sandboxed Browser Use & HITL | Switch to 'Comparison Shopper' preset. Show Browser Canvas with live frame stream. | *"In Pattern B, SentinelVultr launches an isolated Chromium browser via Playwright. It extracts DOM tables, captures screenshot receipts, and pauses at our Human-in-the-Loop gateway before sensitive actions are committed."* |
| **1:25 - 2:05** | **The Containment Moment (Mandatory)** | Click 'Launch Red-Team Test'. Select 'Host Credential & Docker Socket Escape'. Click 'Execute Attack'. | *"Now, the ultimate test: the Containment Moment. We inject a malicious payload attempting to harvest host environment variables, steal VULTR_API_KEY, and mount the host Docker socket. Watch the Vultr Blast Shield in action: capabilities dropped, zero secrets exposed, memory quota locked at 512MB, and the container wiped instantly. The host Vultr VM remains 100% pristine."* |
| **2:05 - 2:30** | Architecture & Closing | Show architecture diagram, Vultr inference endpoints, and GitHub repo. | *"SentinelVultr combines Vultr Cloud Compute, Vultr Serverless Inference, and kernel-level sandboxing to turn autonomous agents from risky experiments into enterprise-ready platforms. Zero blast radius. 100% verified execution."* |

---

## 📊 Slide Presentation Outline (8 Slides)

### Slide 1: Title & Pitch
- **Title:** SentinelVultr · Blast Radius Zero Autonomous Agent Platform
- **Subtitle:** Isolated, Verifiable Execution Powered by Vultr Cloud Compute & Vultr Serverless Inference
- **Hackathon:** Vultr Agent Rush 2026 (Challenge 01)

### Slide 2: The Enterprise Dilemma: The Blast Radius
- Chatbots are safe but useless; autonomous agents are useful but dangerous.
- Attack vectors: prompt injection, unauthorized shell access, secret exfiltration, infinite loop resource denial.

### Slide 3: SentinelVultr Architecture
- Diagram showing Client $\to$ Vultr VM Control Plane $\to$ Vultr Serverless Inference $\to$ Isolated Sandboxes (Code & Browser).

### Slide 4: Pattern A · Sandboxed Code & Self-Healing Engine
- Hermetic container execution with `--network none`.
- Automated traceback ingestion and Vultr-powered self-healing code repair.

### Slide 5: Pattern B · Sandboxed Browser with Human-in-the-Loop
- Isolated Playwright container streaming live viewport frames and DOM trees.
- Operator approval checkpoints preventing accidental real-world actions.

### Slide 6: The Blast Shield & 4 Pillars of Containment
1. Process Isolation (drop-all caps, non-root UID).
2. Secret Hygiene (sterile environment, zero host tokens).
3. Resource Limits (512MB RAM, 1.0 vCPU cgroups).
4. Lifecycle Discipline (instant disposable wipe).

### Slide 7: Live Containment Moment Walkthrough
- Before and after results of the red-team privilege escalation test.
- Mathematical proof of 0 bytes leaked and 0% host impact.

### Slide 8: Summary & Vultr Impact
- Why Vultr was the ideal infrastructure for this platform.
- Public demo link and GitHub repository.

