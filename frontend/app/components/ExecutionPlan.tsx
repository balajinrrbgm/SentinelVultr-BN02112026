"use client";

import React from "react";
import { Brain, CheckCircle2, Loader2, Sparkles, Terminal, Globe, Shield } from "lucide-react";

interface ExecutionPlanProps {
  phase: string;
  progress: number;
  thought: string;
  planSteps: string[];
  actionType: string;
  latencySec?: number;
  modelName?: string;
}

export const ExecutionPlan: React.FC<ExecutionPlanProps> = ({
  phase,
  progress,
  thought,
  planSteps,
  actionType,
  latencySec,
  modelName,
}) => {
  return (
    <div className="bg-[#0b1426] border border-slate-800 rounded-xl p-4 shadow-xl">
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-slate-800/80 mb-3">
        <div className="flex items-center space-x-2">
          <Brain className="w-4 h-4 text-purple-400" />
          <span className="text-xs font-bold text-slate-200 tracking-wide uppercase">
            Vultr Inference Plan & Reasoning DAG
          </span>
        </div>
        <div className="flex items-center space-x-2 text-xs">
          {modelName && (
            <span className="font-mono text-[10px] text-slate-400">
              Model: <span className="text-cyan-300">{modelName}</span>
            </span>
          )}
          {latencySec && (
            <span className="font-mono text-[10px] text-emerald-400 bg-emerald-950/40 px-2 py-0.5 rounded border border-emerald-500/20">
              {latencySec}s
            </span>
          )}
        </div>
      </div>

      {/* Progress Bar */}
      <div className="mb-4">
        <div className="flex justify-between text-xs text-slate-400 mb-1.5 font-mono">
          <span className="flex items-center space-x-1.5">
            {progress < 100 && progress > 0 ? (
              <Loader2 className="w-3.5 h-3.5 text-cyan-400 animate-spin" />
            ) : (
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
            )}
            <span className="text-slate-200 font-semibold">{phase || "READY"}</span>
          </span>
          <span>{progress}%</span>
        </div>
        <div className="w-full bg-slate-900 rounded-full h-2 overflow-hidden border border-slate-800">
          <div
            className="h-full bg-gradient-to-r from-blue-500 via-cyan-400 to-emerald-400 transition-all duration-500 ease-out"
            style={{ width: `${progress}%` }}
          ></div>
        </div>
      </div>

      {/* Agent Thought Box */}
      {thought && (
        <div className="mb-4 p-3 rounded-lg bg-slate-900/90 border border-slate-800 text-xs">
          <div className="flex items-center space-x-1.5 text-cyan-400 font-mono text-[11px] mb-1">
            <Sparkles className="w-3.5 h-3.5" />
            <span className="font-semibold uppercase tracking-wider">Agent Strategic Reasoning:</span>
          </div>
          <p className="text-slate-300 leading-relaxed italic">{thought}</p>
        </div>
      )}

      {/* Plan Steps Pipeline */}
      <div>
        <div className="text-[11px] uppercase tracking-wider font-mono text-slate-400 mb-2 flex items-center justify-between">
          <span>Decomposed Action Sequence:</span>
          <span className="flex items-center space-x-1 text-slate-300">
            {actionType === "execute_browser" ? (
              <>
                <Globe className="w-3.5 h-3.5 text-cyan-400" />
                <span className="text-cyan-300">Pattern B: Browser Sandbox</span>
              </>
            ) : (
              <>
                <Terminal className="w-3.5 h-3.5 text-blue-400" />
                <span className="text-blue-300">Pattern A: Code Sandbox</span>
              </>
            )}
          </span>
        </div>

        <div className="space-y-1.5">
          {planSteps && planSteps.length > 0 ? (
            planSteps.map((step, idx) => (
              <div
                key={idx}
                className="flex items-start space-x-2.5 p-2 rounded-lg bg-slate-900/60 border border-slate-800/80 text-xs"
              >
                <div className="w-4 h-4 rounded-full bg-blue-500/20 text-blue-400 flex items-center justify-center font-mono text-[10px] font-bold mt-0.5">
                  {idx + 1}
                </div>
                <span className="text-slate-300 font-medium">{step}</span>
              </div>
            ))
          ) : (
            <div className="text-xs text-slate-500 italic p-3 text-center border border-dashed border-slate-800 rounded-lg">
              Awaiting mission dispatch to synthesize execution plan...
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

