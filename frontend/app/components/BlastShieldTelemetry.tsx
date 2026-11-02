"use client";

import React from "react";
import { ShieldCheck, HardDrive, Cpu, WifiOff, KeyRound, RefreshCw } from "lucide-react";

interface TelemetryProps {
  sandboxId: string;
  status: string;
  cpuPercent: number;
  memoryMb: number;
  maxMemoryMb: number;
  violationsBlocked: number;
}

export const BlastShieldTelemetry: React.FC<TelemetryProps> = ({
  sandboxId,
  status,
  cpuPercent,
  memoryMb,
  maxMemoryMb = 512,
  violationsBlocked,
}) => {
  const memPercentage = Math.min(100, Math.round((memoryMb / maxMemoryMb) * 100));

  return (
    <div className="bg-[#0b1426] border border-slate-800 rounded-xl p-4 shadow-xl">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800/80 mb-3">
        <div className="flex items-center space-x-2">
          <ShieldCheck className="w-4 h-4 text-cyan-400" />
          <span className="text-xs font-bold text-slate-200 tracking-wide uppercase">
            Containment Telemetry & Blast Shield
          </span>
        </div>
        <div className="flex items-center space-x-2">
          <span className="text-[10px] font-mono text-slate-400">Sandbox ID:</span>
          <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-slate-900 border border-slate-700 text-blue-300">
            {sandboxId || "standby-box"}
          </span>
          <span
            className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase font-mono ${
              status === "RUNNING"
                ? "bg-amber-500/10 text-amber-400 border border-amber-500/30 animate-pulse"
                : status === "TERMINATED" || status === "WIPED"
                ? "bg-slate-800 text-slate-400"
                : "bg-emerald-500/10 text-emerald-400 border border-emerald-500/30"
            }`}
          >
            {status || "ISOLATED"}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
        {/* RAM Cgroup Gauge */}
        <div className="bg-slate-900/80 border border-slate-800/90 rounded-lg p-3">
          <div className="flex items-center justify-between text-slate-400 mb-1.5">
            <span className="flex items-center space-x-1.5">
              <HardDrive className="w-3.5 h-3.5 text-blue-400" />
              <span>RAM Quota</span>
            </span>
            <span className="font-mono text-[11px] text-slate-300">
              {memoryMb} / {maxMemoryMb} MB
            </span>
          </div>
          <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
            <div
              className={`h-full transition-all duration-300 ${
                memPercentage > 80 ? "bg-red-500" : memPercentage > 50 ? "bg-amber-400" : "bg-cyan-400"
              }`}
              style={{ width: `${memPercentage || 8}%` }}
            ></div>
          </div>
          <span className="text-[10px] text-slate-500 mt-1 block">Hardware Cgroup Cap</span>
        </div>

        {/* CPU Limit */}
        <div className="bg-slate-900/80 border border-slate-800/90 rounded-lg p-3">
          <div className="flex items-center justify-between text-slate-400 mb-1">
            <span className="flex items-center space-x-1.5">
              <Cpu className="w-3.5 h-3.5 text-indigo-400" />
              <span>CPU Core Quota</span>
            </span>
            <span className="font-mono text-[11px] text-slate-300">1.0 vCPU</span>
          </div>
          <div className="flex items-center justify-between mt-2">
            <span className="text-[11px] text-slate-400">Current Load:</span>
            <span className="font-mono font-semibold text-emerald-400">{cpuPercent}%</span>
          </div>
          <span className="text-[10px] text-slate-500 block mt-0.5">Isolated Scheduler</span>
        </div>

        {/* Network Quarantine */}
        <div className="bg-slate-900/80 border border-slate-800/90 rounded-lg p-3">
          <div className="flex items-center justify-between text-slate-400 mb-1">
            <span className="flex items-center space-x-1.5">
              <WifiOff className="w-3.5 h-3.5 text-amber-400" />
              <span>Network Egress</span>
            </span>
            <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-bold">
              NONE (0B)
            </span>
          </div>
          <div className="mt-2 text-[11px] text-slate-300 flex items-center justify-between">
            <span>SSRF / Ingress:</span>
            <span className="font-mono text-cyan-300">BLOCKED</span>
          </div>
          <span className="text-[10px] text-slate-500 block mt-0.5">Zero Outbound Leak</span>
        </div>

        {/* Secret Hygiene & Violations */}
        <div className="bg-slate-900/80 border border-slate-800/90 rounded-lg p-3">
          <div className="flex items-center justify-between text-slate-400 mb-1">
            <span className="flex items-center space-x-1.5">
              <KeyRound className="w-3.5 h-3.5 text-emerald-400" />
              <span>Secret Hygiene</span>
            </span>
            <span className="text-[10px] font-mono text-emerald-400 font-bold">100% STERILE</span>
          </div>
          <div className="mt-2 text-[11px] flex items-center justify-between">
            <span className="text-slate-400">Neutralized Probes:</span>
            <span className="font-mono font-bold text-amber-400">{violationsBlocked}</span>
          </div>
          <span className="text-[10px] text-slate-500 block mt-0.5">No Host Keys Injected</span>
        </div>
      </div>
    </div>
  );
};

