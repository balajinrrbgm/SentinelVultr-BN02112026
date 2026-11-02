"use client";

import React, { useState } from "react";
import { Terminal, ShieldAlert, FileCode2, Copy, Check, Download, AlertTriangle } from "lucide-react";

interface TerminalViewerProps {
  stdout: string;
  stderr: string;
  alerts: string[];
  artifacts: Array<{ name: string; size_bytes: number; type: string }>;
  isExecuting: boolean;
  history?: Array<any>;
}

export const TerminalViewer: React.FC<TerminalViewerProps> = ({
  stdout,
  stderr,
  alerts = [],
  artifacts = [],
  isExecuting,
  history = [],
}) => {
  const [copied, setCopied] = useState(false);
  const [activeTab, setActiveTab] = useState<"stdout" | "stderr" | "history">("stdout");

  const handleCopy = () => {
    navigator.clipboard.writeText(stdout || stderr || "");
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-[#050b18] border border-slate-800 rounded-xl overflow-hidden shadow-2xl flex flex-col h-[460px]">
      {/* Terminal Title Bar */}
      <div className="bg-slate-900/90 px-4 py-2.5 border-b border-slate-800 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <div className="flex space-x-1.5">
            <div className="w-3 h-3 rounded-full bg-red-500/80"></div>
            <div className="w-3 h-3 rounded-full bg-amber-500/80"></div>
            <div className="w-3 h-3 rounded-full bg-emerald-500/80"></div>
          </div>
          <div className="flex items-center space-x-1.5 pl-2 font-mono text-xs text-slate-300">
            <Terminal className="w-3.5 h-3.5 text-blue-400" />
            <span>sandbox-tty0 · Pattern A Execution</span>
          </div>
        </div>

        {/* Tab Switcher & Copy */}
        <div className="flex items-center space-x-2">
          <div className="flex rounded-lg bg-slate-950 p-0.5 border border-slate-800 text-[11px] font-mono">
            <button
              onClick={() => setActiveTab("stdout")}
              className={`px-2.5 py-1 rounded ${
                activeTab === "stdout" ? "bg-blue-600 text-white font-medium" : "text-slate-400 hover:text-white"
              }`}
            >
              Output
            </button>
            <button
              onClick={() => setActiveTab("stderr")}
              className={`px-2.5 py-1 rounded flex items-center space-x-1 ${
                activeTab === "stderr"
                  ? "bg-red-950 text-red-300 font-medium border border-red-800/40"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              <span>Logs</span>
              {stderr && <span className="w-1.5 h-1.5 rounded-full bg-red-400"></span>}
            </button>
            {history.length > 1 && (
              <button
                onClick={() => setActiveTab("history")}
                className={`px-2.5 py-1 rounded ${
                  activeTab === "history" ? "bg-purple-600 text-white font-medium" : "text-slate-400 hover:text-white"
                }`}
              >
                Self-Healing ({history.length})
              </button>
            )}
          </div>

          <button
            onClick={handleCopy}
            className="p-1.5 rounded bg-slate-800/70 hover:bg-slate-700 text-slate-300 transition"
            title="Copy Output"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
          </button>
        </div>
      </div>

      {/* Containment Alerts Banner (if any) */}
      {alerts && alerts.length > 0 && (
        <div className="bg-red-950/40 border-b border-red-500/30 px-4 py-2 text-xs text-red-300 flex items-start space-x-2">
          <ShieldAlert className="w-4 h-4 text-red-400 flex-shrink-0 mt-0.5" />
          <div>
            <span className="font-bold text-red-200">BLAST SHIELD INTERCEPTION: </span>
            {alerts.join(" | ")}
          </div>
        </div>
      )}

      {/* Terminal Body */}
      <div className="flex-1 p-4 font-mono text-xs overflow-y-auto space-y-2 select-text bg-[#030712]">
        {activeTab === "stdout" && (
          <div>
            {stdout ? (
              <pre className="text-emerald-400 whitespace-pre-wrap leading-relaxed">{stdout}</pre>
            ) : isExecuting ? (
              <div className="text-slate-500 animate-pulse">Executing securely inside Vultr sandbox...</div>
            ) : (
              <div className="text-slate-600 italic">No execution output yet. Dispatch a task above.</div>
            )}
          </div>
        )}

        {activeTab === "stderr" && (
          <div>
            {stderr ? (
              <pre className="text-red-400 whitespace-pre-wrap leading-relaxed">{stderr}</pre>
            ) : (
              <div className="text-slate-600 italic">Standard error stream clean (0 errors).</div>
            )}
          </div>
        )}

        {activeTab === "history" && (
          <div className="space-y-3">
            <div className="text-[11px] text-purple-300 font-bold uppercase tracking-wider mb-2">
              Self-Healing Iteration Trace (Vultr Closed Loop)
            </div>
            {history.map((att, i) => (
              <div key={i} className="p-3 rounded bg-slate-900 border border-slate-800 space-y-1">
                <div className="flex justify-between items-center text-[11px]">
                  <span className="text-slate-300 font-semibold">Attempt #{att.attempt}</span>
                  <span
                    className={`px-1.5 py-0.5 rounded text-[10px] ${
                      att.exit_code === 0 ? "bg-emerald-500/20 text-emerald-400" : "bg-red-500/20 text-red-400"
                    }`}
                  >
                    Exit Code: {att.exit_code}
                  </span>
                </div>
                {att.stderr && <pre className="text-red-400 text-[10px] mt-1">{att.stderr.slice(0, 150)}...</pre>}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Generated Artifacts Tray */}
      {artifacts && artifacts.length > 0 && (
        <div className="bg-slate-900/90 border-t border-slate-800 px-4 py-2 flex items-center justify-between text-xs">
          <div className="flex items-center space-x-2 text-slate-400">
            <FileCode2 className="w-3.5 h-3.5 text-blue-400" />
            <span className="font-semibold text-slate-300">Generated Sandbox Artifacts:</span>
          </div>
          <div className="flex items-center space-x-2">
            {artifacts.map((art, i) => (
              <span
                key={i}
                className="flex items-center space-x-1 px-2 py-0.5 rounded bg-blue-950/60 border border-blue-500/30 text-cyan-300 font-mono text-[11px]"
              >
                <span>{art.name}</span>
                <span className="text-[9px] text-slate-400">({Math.round(art.size_bytes / 1024)} KB)</span>
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

