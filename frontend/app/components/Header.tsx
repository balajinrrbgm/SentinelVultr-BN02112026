"use client";

import React from "react";
import { Shield, Cpu, Activity, AlertTriangle, ExternalLink, Flame } from "lucide-react";

interface HeaderProps {
  onOpenContainmentModal: () => void;
  isSandboxedActive: boolean;
}

export const Header: React.FC<HeaderProps> = ({ onOpenContainmentModal, isSandboxedActive }) => {
  return (
    <header className="border-b border-slate-800 bg-[#0a1226]/80 backdrop-blur sticky top-0 z-40 px-6 py-3.5 flex items-center justify-between">
      {/* Brand & Identity */}
      <div className="flex items-center space-x-3.5">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-[#007BFC] to-[#00E5FF] flex items-center justify-center shadow-lg shadow-blue-500/20">
          <Shield className="w-6 h-6 text-white" />
        </div>
        <div>
          <div className="flex items-center space-x-2">
            <h1 className="text-lg font-bold text-white tracking-tight">SentinelVultr</h1>
            <span className="text-[10px] uppercase font-mono tracking-wider px-2 py-0.5 rounded-full bg-blue-500/10 text-cyan-400 border border-blue-500/30">
              Blast Radius Zero
            </span>
          </div>
          <p className="text-xs text-slate-400">
            Isolated Autonomous Agent Control Plane · Powered by Vultr Cloud Compute
          </p>
        </div>
      </div>

      {/* Vultr Tech Stack Badges & Live Status */}
      <div className="flex items-center space-x-3">
        {/* Vultr Serverless Inference Badge */}
        <div className="hidden md:flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs">
          <Cpu className="w-3.5 h-3.5 text-blue-400" />
          <span className="text-slate-400">Inference:</span>
          <span className="font-mono text-cyan-300 font-medium">Llama-3.3-70B</span>
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        </div>

        {/* Blast Shield Status */}
        <div className="flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-emerald-950/40 border border-emerald-500/30 text-xs text-emerald-400">
          <Activity className="w-3.5 h-3.5 text-emerald-400" />
          <span className="font-medium">Blast Shield: ARMED</span>
          <span className="text-[10px] font-mono text-emerald-300">(0 Leaks)</span>
        </div>

        {/* Containment Moment Trigger Button (Showstopper for Judges) */}
        <button
          onClick={onOpenContainmentModal}
          className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-gradient-to-r from-red-600 to-rose-700 hover:from-red-500 hover:to-rose-600 text-white text-xs font-semibold shadow-lg shadow-red-900/40 transition-all transform hover:scale-[1.02] active:scale-[0.98]"
        >
          <Flame className="w-3.5 h-3.5 text-amber-300 animate-bounce" />
          <span>Launch Red-Team Test</span>
        </button>
      </div>
    </header>
  );
};

