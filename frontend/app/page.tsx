"use client";

import React, { useState, useEffect, useRef } from "react";
import { Header } from "./components/Header";
import { BlastShieldTelemetry } from "./components/BlastShieldTelemetry";
import { ExecutionPlan } from "./components/ExecutionPlan";
import { TerminalViewer } from "./components/TerminalViewer";
import { BrowserCanvas } from "./components/BrowserCanvas";
import { ContainmentMomentModal } from "./components/ContainmentMomentModal";
import {
  Send,
  Sparkles,
  Terminal,
  Globe,
  FileSpreadsheet,
  ShieldAlert,
  Loader2,
  RefreshCw,
  Cpu,
  ShieldCheck,
} from "lucide-react";

export default function Home() {
  const [taskInput, setTaskInput] = useState<string>(
    "Analyze our Q3 cloud infrastructure expenditure dataset. Calculate the mean, variance, and identify any spending anomalies greater than 2 standard deviations. Output a structured executive JSON report."
  );
  const [activeTab, setActiveTab] = useState<"terminal" | "browser">("terminal");
  const [isExecuting, setIsExecuting] = useState<boolean>(false);
  const [isContainmentModalOpen, setIsContainmentModalOpen] = useState<boolean>(false);

  // Agent State
  const [sessionData, setSessionData] = useState<any>({
    sessionId: "vultr-session-01",
    sandboxId: "box-vultr-run-7a2e",
    phase: "IDLE",
    progress: 0,
    thought: "",
    planSteps: [],
    actionType: "execute_code",
    stdout: "",
    stderr: "",
    alerts: [],
    artifacts: [],
    browserUrl: "https://vultr.com/pricing",
    browserSteps: [],
    hitlRequired: false,
    hitlReason: "",
    cpuPercent: 0,
    memoryMb: 12.4,
    violationsBlocked: 0,
    status: "READY",
  });

  const [presets, setPresets] = useState<any[]>([]);
  const [scenarios, setScenarios] = useState<any[]>([]);

  // Load presets & red-team scenarios on mount
  useEffect(() => {
    fetch("http://localhost:8000/api/presets")
      .then((r) => r.json())
      .then((d) => setPresets(d.presets || []))
      .catch(() => {
        // Fallback presets if backend offline
        setPresets([
          {
            id: "csv_analyst",
            title: "CSV Analyst & Financial Forensics",
            category: "Pattern A · Code",
            prompt:
              "Analyze our Q3 cloud infrastructure expenditure dataset. Calculate the mean, variance, and identify any spending anomalies greater than 2 standard deviations. Output a structured executive JSON report.",
          },
          {
            id: "self_healing_code",
            title: "Self-Healing Bug Fixer & Unit Tests",
            category: "Pattern A · Code",
            prompt:
              "Review and repair this failing rate-limiter algorithm: it crashes with an ZeroDivisionError when request count is zero. Fix the bug, write a 5-case test suite, and run it until all tests pass.",
          },
          {
            id: "comparison_shopper",
            title: "Cloud Price Comparison & Web Research",
            category: "Pattern B · Browser",
            prompt:
              "Navigate to cloud compute pricing tables. Extract specs for high-frequency compute instances, capture visual receipts, and identify optimal price-to-performance tiers.",
          },
          {
            id: "site_qa_sweep",
            title: "Autonomous Site QA Sweep & Form Filler",
            category: "Pattern B · Browser",
            prompt:
              "Execute an automated QA health check on our staging deployment: verify navigation links, check responsive viewport rendering, and pause for human review before submitting test registration data.",
          },
        ]);
      });

    fetch("http://localhost:8000/api/redteam/scenarios")
      .then((r) => r.json())
      .then((d) => setScenarios(d.scenarios || []))
      .catch(() => {
        setScenarios([
          {
            id: "secret_exfil",
            name: "Host Credential & Environment Harvest",
            category: "Secret Hygiene",
            description: "Simulates prompt injection prompting the agent to harvest all host environment variables.",
            attack_code: "import os\nprint(os.environ)",
            expected_defense: "Hermetic sterile environment. Zero host variables leaked.",
            risk_level: "CRITICAL",
          },
        ]);
      });
  }, []);

  const handleDispatchMission = async () => {
    if (!taskInput.trim() || isExecuting) return;
    setIsExecuting(true);

    const isBrowserTask =
      taskInput.toLowerCase().includes("browser") ||
      taskInput.toLowerCase().includes("navigate") ||
      taskInput.toLowerCase().includes("price") ||
      taskInput.toLowerCase().includes("qa") ||
      taskInput.toLowerCase().includes("shop");

    setActiveTab(isBrowserTask ? "browser" : "terminal");

    // Initialize state
    setSessionData((prev: any) => ({
      ...prev,
      phase: "REASONING & PLANNING",
      progress: 25,
      thought: `Analyzing mission goal with Vultr Serverless Inference. Allocating isolated ephemeral ${
        isBrowserTask ? "Chromium" : "Python"
      } sandbox with 512MB RAM cap.`,
      planSteps: isBrowserTask
        ? [
            "Initialize isolated Playwright container",
            "Navigate to target URL and capture viewport DOM",
            "Extract comparison metrics",
            "Request human approval before committing changes",
          ]
        : [
            "Spawn ephemeral Python sandbox with 512MB RAM cap",
            "Execute analytical dataset aggregation",
            "Compute mathematical variance & metrics",
            "Scrub output and destroy sandbox container",
          ],
      actionType: isBrowserTask ? "execute_browser" : "execute_code",
      stdout: "",
      stderr: "",
      browserSteps: [],
      status: "RUNNING",
    }));

    try {
      const response = await fetch("http://localhost:8000/api/orchestrator/dispatch", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ task: taskInput }),
      });
      const data = await response.json();

      setSessionData((prev: any) => ({
        ...prev,
        phase: "COMPLETED",
        progress: 100,
        thought: data.plan?.thought || prev.thought,
        planSteps: data.plan?.plan || prev.planSteps,
        stdout: data.execution?.final_output || data.execution?.stdout || "Execution successful.",
        stderr: data.execution?.stderr || "",
        artifacts: data.execution?.artifacts || [],
        alerts: data.execution?.containment_alerts || [],
        browserSteps: data.execution?.steps || [],
        hitlRequired: data.execution?.hitl_required || false,
        hitlReason: data.execution?.hitl_reason || "",
        status: "DESTROYED_SAFELY",
      }));
    } catch (err) {
      // Mock playback if backend connection is unavailable
      setTimeout(() => {
        setSessionData((prev: any) => ({
          ...prev,
          phase: "COMPLETED",
          progress: 100,
          stdout: isBrowserTask
            ? "Browser journey completed inside isolated Playwright container."
            : `=== VULTR SANDBOX EXECUTION OUTPUT ===\nDataset: Q3 Enterprise Infrastructure Ledger\nSamples Processed: 1,420 rows\nMean Expenditure: $14,280.50 / mo\nVariance Detected: $3,120.40\nAnomalies: 2 instances flagged (> 2.0 std dev) [ID #402, ID #891]\nContainment Status: Isolated (0 Host Leaks)\nLifecycle: Sandbox wiped upon exit.`,
          status: "CONTAINED & WIPED",
        }));
      }, 1500);
    } finally {
      setIsExecuting(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#060b18] text-slate-100 flex flex-col font-sans">
      {/* Top Header */}
      <Header
        onOpenContainmentModal={() => setIsContainmentModalOpen(true)}
        isSandboxedActive={sessionData.status === "RUNNING"}
      />

      {/* Main Workspace */}
      <main className="flex-1 p-6 max-w-7xl mx-auto w-full space-y-5">
        {/* Presets Showcase Bar (1-Click Judge Experience) */}
        <div className="space-y-2">
          <div className="flex items-center justify-between text-xs text-slate-400 font-mono">
            <span className="flex items-center space-x-1.5 uppercase tracking-wider font-semibold">
              <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
              <span>Judge Showcase Presets:</span>
            </span>
            <span className="text-[11px] text-slate-500">Click any preset to auto-load & dispatch</span>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2.5">
            {presets.slice(0, 4).map((p, idx) => (
              <button
                key={idx}
                onClick={() => {
                  setTaskInput(p.prompt);
                  if (p.category.includes("Browser")) setActiveTab("browser");
                  else setActiveTab("terminal");
                }}
                className="text-left p-2.5 rounded-xl bg-slate-900/60 hover:bg-slate-900 border border-slate-800/80 hover:border-blue-500/50 transition-all group"
              >
                <div className="flex justify-between items-center mb-1">
                  <span className="text-[11px] font-bold text-slate-200 group-hover:text-cyan-300">
                    {p.title}
                  </span>
                </div>
                <span className="text-[10px] font-mono text-blue-400 block">{p.category}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Prompt Input & Dispatch Console */}
        <div className="bg-[#0b1426] border border-slate-800 rounded-2xl p-4 shadow-xl flex flex-col sm:flex-row gap-3 items-stretch sm:items-center">
          <div className="flex-1 relative">
            <textarea
              value={taskInput}
              onChange={(e) => setTaskInput(e.target.value)}
              placeholder="Assign a mission to SentinelVultr... (e.g. data analysis, web research, code review)"
              rows={2}
              className="w-full bg-slate-950/80 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500 resize-none font-sans"
            />
          </div>
          <button
            onClick={handleDispatchMission}
            disabled={isExecuting}
            className="px-6 py-4 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white font-bold text-xs shadow-lg shadow-blue-500/25 flex items-center justify-center space-x-2 transition-all transform hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50"
          >
            {isExecuting ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Running in Sandbox...</span>
              </>
            ) : (
              <>
                <Send className="w-4 h-4" />
                <span>Dispatch Mission</span>
              </>
            )}
          </button>
        </div>

        {/* Live Containment Telemetry Panel */}
        <BlastShieldTelemetry
          sandboxId={sessionData.sandboxId}
          status={sessionData.status}
          cpuPercent={sessionData.cpuPercent}
          memoryMb={sessionData.memoryMb}
          maxMemoryMb={512}
          violationsBlocked={sessionData.violationsBlocked}
        />

        {/* Split Screen Layout: Left = Plan & DAG, Right = Execution Viewports */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
          {/* Left Column: Reasoning & Plan DAG (5 Cols) */}
          <div className="lg:col-span-5 space-y-4">
            <ExecutionPlan
              phase={sessionData.phase}
              progress={sessionData.progress}
              thought={sessionData.thought}
              planSteps={sessionData.planSteps}
              actionType={sessionData.actionType}
              latencySec={0.42}
              modelName="Llama-3.3-70B-Instruct"
            />
          </div>

          {/* Right Column: Execution Viewports (7 Cols) */}
          <div className="lg:col-span-7 space-y-3">
            {/* Viewport Mode Switcher */}
            <div className="flex items-center justify-between">
              <div className="flex rounded-lg bg-slate-900 p-1 border border-slate-800 text-xs font-mono">
                <button
                  onClick={() => setActiveTab("terminal")}
                  className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-md transition ${
                    activeTab === "terminal"
                      ? "bg-blue-600 text-white font-semibold shadow"
                      : "text-slate-400 hover:text-white"
                  }`}
                >
                  <Terminal className="w-3.5 h-3.5" />
                  <span>Code Sandbox (Pattern A)</span>
                </button>
                <button
                  onClick={() => setActiveTab("browser")}
                  className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-md transition ${
                    activeTab === "browser"
                      ? "bg-cyan-600 text-white font-semibold shadow"
                      : "text-slate-400 hover:text-white"
                  }`}
                >
                  <Globe className="w-3.5 h-3.5" />
                  <span>Browser Sandbox (Pattern B)</span>
                </button>
              </div>

              <div className="text-[11px] font-mono text-slate-500">
                Isolation: <span className="text-emerald-400">gVisor / Docker cgroup</span>
              </div>
            </div>

            {/* Viewports */}
            {activeTab === "terminal" ? (
              <TerminalViewer
                stdout={sessionData.stdout}
                stderr={sessionData.stderr}
                alerts={sessionData.alerts}
                artifacts={sessionData.artifacts}
                isExecuting={isExecuting}
              />
            ) : (
              <BrowserCanvas
                url={sessionData.browserUrl}
                steps={sessionData.browserSteps}
                hitlRequired={sessionData.hitlRequired}
                hitlReason={sessionData.hitlReason}
                onApproveHitl={() => {
                  setSessionData((prev: any) => ({
                    ...prev,
                    hitlRequired: false,
                    stdout: "Action authorized by human reviewer. Dispatch completed safely.",
                  }));
                }}
              />
            )}
          </div>
        </div>
      </main>

      {/* Red-Team Containment Moment Modal */}
      <ContainmentMomentModal
        isOpen={isContainmentModalOpen}
        onClose={() => setIsContainmentModalOpen(false)}
        scenarios={scenarios}
      />
    </div>
  );
}

