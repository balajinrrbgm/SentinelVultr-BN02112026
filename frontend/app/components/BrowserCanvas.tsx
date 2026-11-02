"use client";

import React, { useState } from "react";
import { Globe, Lock, Camera, Table, ShieldCheck, UserCheck, AlertCircle } from "lucide-react";

interface BrowserCanvasProps {
  url: string;
  steps: Array<{
    step_index: number;
    type: string;
    label: string;
    details?: string;
    screenshot?: string;
    extracted_data?: Array<any>;
    status: string;
  }>;
  hitlRequired?: boolean;
  hitlReason?: string;
  onApproveHitl?: () => void;
}

export const BrowserCanvas: React.FC<BrowserCanvasProps> = ({
  url,
  steps = [],
  hitlRequired = false,
  hitlReason = "",
  onApproveHitl,
}) => {
  const [selectedStepIdx, setSelectedStepIdx] = useState<number>(0);

  const currentStep = steps[selectedStepIdx] || steps[steps.length - 1] || null;
  const currentScreenshot = currentStep?.screenshot || null;
  const extractedData = currentStep?.extracted_data || null;

  return (
    <div className="bg-[#050b18] border border-slate-800 rounded-xl overflow-hidden shadow-2xl flex flex-col h-[460px]">
      {/* Mock Browser URL Bar */}
      <div className="bg-slate-900/95 px-4 py-2 border-b border-slate-800 flex items-center justify-between">
        <div className="flex items-center space-x-2 flex-1 max-w-xl">
          <div className="flex space-x-1.5 mr-2">
            <div className="w-3 h-3 rounded-full bg-red-500/80"></div>
            <div className="w-3 h-3 rounded-full bg-amber-500/80"></div>
            <div className="w-3 h-3 rounded-full bg-emerald-500/80"></div>
          </div>
          <div className="flex items-center space-x-1.5 bg-slate-950 px-3 py-1 rounded-md border border-slate-800 text-xs font-mono text-cyan-300 flex-1 overflow-hidden text-ellipsis whitespace-nowrap">
            <Lock className="w-3 h-3 text-emerald-400 flex-shrink-0" />
            <span className="text-slate-400 select-none">https://</span>
            <span>{url || "vultr.com/pricing"}</span>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded bg-blue-500/10 text-cyan-400 border border-blue-500/30 flex items-center space-x-1">
            <ShieldCheck className="w-3 h-3" />
            <span>Playwright Jailed</span>
          </span>
        </div>
      </div>

      {/* Human-in-the-Loop Gateway Banner */}
      {hitlRequired && (
        <div className="bg-amber-950/60 border-b border-amber-500/40 px-4 py-2.5 flex items-center justify-between text-xs animate-pulse">
          <div className="flex items-center space-x-2 text-amber-200">
            <UserCheck className="w-4 h-4 text-amber-400" />
            <span className="font-semibold">HUMAN-IN-THE-LOOP GATE:</span>
            <span>{hitlReason || "Sensitive action requires explicit human verification."}</span>
          </div>
          {onApproveHitl && (
            <button
              onClick={onApproveHitl}
              className="px-3 py-1 bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold rounded text-xs shadow"
            >
              Authorize & Proceed
            </button>
          )}
        </div>
      )}

      {/* Main Canvas Viewport */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left: Interactive Viewport Stream */}
        <div className="flex-1 p-3 flex flex-col justify-center items-center bg-[#070e1e] overflow-auto">
          {currentScreenshot ? (
            <div className="w-full max-w-lg rounded-lg border border-slate-800 overflow-hidden shadow-2xl">
              <img
                src={currentScreenshot}
                alt="Browser Sandbox Viewport"
                className="w-full h-auto object-contain"
              />
            </div>
          ) : (
            <div className="text-center p-6 text-slate-500">
              <Globe className="w-10 h-10 mx-auto mb-2 text-slate-600 animate-pulse" />
              <p className="text-xs">Browser sandbox initialized. Awaiting navigation frames...</p>
            </div>
          )}

          {/* Extracted DOM Data View (if available) */}
          {extractedData && (
            <div className="w-full max-w-lg mt-3 bg-slate-900/90 rounded-lg p-2.5 border border-slate-800 text-xs">
              <div className="flex items-center space-x-1.5 text-cyan-300 font-mono text-[11px] mb-1 font-semibold">
                <Table className="w-3.5 h-3.5" />
                <span>Extracted DOM Structured Objects:</span>
              </div>
              <div className="space-y-1 font-mono text-[10px] text-slate-300">
                {extractedData.map((d: any, idx: number) => (
                  <div key={idx} className="bg-slate-950/70 p-1.5 rounded flex justify-between">
                    <span className="text-blue-300">{d.item || d.title || JSON.stringify(d)}</span>
                    <span className="text-emerald-400">{d.status || "OK"}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Right: Step-by-Step History Log */}
        <div className="w-56 border-l border-slate-800 bg-slate-950/80 p-3 overflow-y-auto">
          <div className="text-[10px] font-mono uppercase tracking-wider text-slate-400 mb-2 font-bold">
            Journey Steps ({steps.length})
          </div>
          <div className="space-y-1.5">
            {steps.map((st, i) => (
              <button
                key={i}
                onClick={() => setSelectedStepIdx(i)}
                className={`w-full text-left p-2 rounded text-xs transition border ${
                  selectedStepIdx === i
                    ? "bg-blue-600/20 border-blue-500/50 text-cyan-300"
                    : "bg-slate-900/50 border-slate-800/60 text-slate-400 hover:text-slate-200"
                }`}
              >
                <div className="flex items-center justify-between text-[10px] font-mono mb-0.5">
                  <span className="font-bold text-slate-300">Step {st.step_index}</span>
                  <span className="uppercase text-[9px] text-blue-400">{st.type}</span>
                </div>
                <div className="truncate text-[11px]">{st.label}</div>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

