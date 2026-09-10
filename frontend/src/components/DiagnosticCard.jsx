import React from 'react';
import { ShieldAlert, CheckCircle2, Cpu, Crosshair, Sparkles } from 'lucide-react';

export default function DiagnosticCard({ mlPrediction }) {
  if (!mlPrediction) return null;

  const { has_issue, isolated_location, confidence_score, fault_code, severity, subsystem, pinn_transformer } = mlPrediction;

  const getSeverityBadge = (sev) => {
    switch (sev) {
      case "CRITICAL":
        return "bg-red-500/20 text-red-300 border-red-500/40";
      case "HIGH":
        return "bg-orange-500/20 text-orange-300 border-orange-500/40";
      case "MEDIUM":
        return "bg-amber-500/20 text-amber-300 border-amber-500/40";
      default:
        return "bg-emerald-500/20 text-emerald-300 border-emerald-500/40";
    }
  };

  return (
    <div className="bg-[#161b22] border border-[#30363d] rounded-none p-5 shadow-sm">
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-[#30363d]">
        <h2 className="text-base font-semibold text-white flex items-center gap-2">
          <Crosshair className="w-5 h-5 text-cyan-400" />
          PINN PyTorch Transformer & ML Diagnostic Output Summary
        </h2>
        <div className="flex items-center gap-2">
          <span className="text-[11px] font-mono bg-cyan-500/10 text-cyan-300 px-2.5 py-0.5 border border-cyan-500/30 flex items-center gap-1 rounded-none">
            <Cpu className="w-3 h-3 text-cyan-400" />
            <span>PyTorch PINN Model Built from Scratch</span>
          </span>
          <span className={`text-xs font-mono font-bold px-3 py-1 border rounded-none ${getSeverityBadge(severity)}`}>
            Severity: {severity}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {/* Output 1: Issue / No Issue Status */}
        <div className={`p-4 border rounded-none flex flex-col justify-between ${
          has_issue
            ? "border-red-500/40 bg-red-950/20 text-white"
            : "border-emerald-500/40 bg-emerald-950/20 text-white"
        }`}>
          <div className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">
            1. System Issue Status
          </div>
          <div className="flex items-center gap-3 my-2">
            {has_issue ? (
              <ShieldAlert className="w-8 h-8 text-red-400 shrink-0 animate-pulse" />
            ) : (
              <CheckCircle2 className="w-8 h-8 text-emerald-400 shrink-0" />
            )}
            <div>
              <div className={`text-lg font-bold ${has_issue ? "text-red-400" : "text-emerald-400"}`}>
                {has_issue ? "ISSUE DETECTED" : "NO ISSUE"}
              </div>
              <div className="text-xs text-gray-300 font-mono">{fault_code}</div>
            </div>
          </div>
          <div className="text-[11px] text-gray-400 border-t border-current/20 pt-2">
            Subsystem: <span className="text-white font-medium">{subsystem}</span>
          </div>
        </div>

        {/* Output 2: Isolated Fault Location */}
        <div className="p-4 border border-[#30363d] bg-[#0d1117] rounded-none flex flex-col justify-between">
          <div className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">
            2. Isolated Problem Location
          </div>
          <div className="my-2">
            <div className="text-sm font-bold text-cyan-300 flex items-start gap-2">
              <Crosshair className="w-4 h-4 text-cyan-400 shrink-0 mt-0.5" />
              <span>{isolated_location}</span>
            </div>
          </div>
          <div className="text-[11px] text-gray-400 border-t border-[#30363d] pt-2">
            Targeted for OEM Repair Workflow
          </div>
        </div>

        {/* Output 3: Overall Ensemble Confidence */}
        <div className="p-4 border border-[#30363d] bg-[#0d1117] rounded-none flex flex-col justify-between">
          <div className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">
            3. Overall Confidence Score
          </div>
          <div className="my-2">
            <div className="flex items-baseline justify-between mb-1.5">
              <span className="text-2xl font-black text-white font-mono">{confidence_score}%</span>
              <span className="text-xs text-cyan-400 font-mono">Ensemble</span>
            </div>
            <div className="w-full h-2.5 bg-[#161b22] border border-[#30363d] rounded-none overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-cyan-500 to-emerald-400 transition-all duration-500 rounded-none"
                style={{ width: `${confidence_score}%` }}
              />
            </div>
          </div>
          <div className="text-[11px] text-gray-400 border-t border-[#30363d] pt-2">
            Physics + ML Multi-Model Agreement
          </div>
        </div>

        {/* Output 4: Custom PyTorch PINN Telemetry Transformer Score */}
        <div className="p-4 border border-cyan-500/40 bg-cyan-950/20 rounded-none flex flex-col justify-between">
          <div className="text-xs font-semibold text-cyan-400 uppercase tracking-wider mb-1 flex items-center gap-1">
            <Sparkles className="w-3.5 h-3.5" />
            4. Custom PyTorch PINN Score
          </div>
          <div className="my-2">
            <div className="flex items-baseline justify-between mb-1.5">
              <span className="text-2xl font-black text-cyan-300 font-mono">
                {pinn_transformer?.pinn_confidence_score || confidence_score}%
              </span>
              <span className="text-xs text-emerald-400 font-mono">
                {pinn_transformer?.pinn_device || "CUDA"}
              </span>
            </div>
            <div className="w-full h-2.5 bg-[#161b22] border border-cyan-500/30 rounded-none overflow-hidden">
              <div
                className="h-full bg-cyan-400 transition-all duration-500 rounded-none"
                style={{ width: `${pinn_transformer?.pinn_confidence_score || confidence_score}%` }}
              />
            </div>
          </div>
          <div className="text-[11px] text-gray-300 border-t border-cyan-500/20 pt-2 font-mono truncate">
            Top: {pinn_transformer?.pinn_top_class || fault_code}
          </div>
        </div>
      </div>
    </div>
  );
}
