import React from 'react';
import { Cpu, Gauge, Zap, Wrench } from 'lucide-react';

export default function Header({ hardwareInfo }) {
  return (
    <header className="border-b border-[#30363d] bg-[#161b22] px-6 py-4 sticky top-0 z-50 shadow-md">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-cyan-500/10 border border-cyan-500/30 rounded-xl text-cyan-400">
            <Gauge className="w-7 h-7 animate-pulse" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-wide text-white flex items-center gap-2">
              I6 ENGINE LLM DIAGNOSTIC SYSTEM
              <span className="text-xs font-mono font-semibold px-2.5 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-500/40">
                v1.0 Physics-ML
              </span>
            </h1>
            <p className="text-xs text-gray-400 flex items-center gap-2 mt-0.5">
              <span>Inline-6 Engine Telemetry</span>
              <span>•</span>
              <span className="font-mono text-cyan-400">Firing Order: 1-5-3-6-2-4</span>
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 text-xs">
          <div className="flex items-center gap-2 bg-[#0d1117] border border-[#30363d] px-3 py-1.5 rounded-lg text-emerald-400 font-mono">
            <Zap className="w-3.5 h-3.5 fill-emerald-400" />
            <span>{hardwareInfo || "NVIDIA GPU / Hugging Face Backend Active"}</span>
          </div>
          <div className="flex items-center gap-2 bg-[#0d1117] border border-[#30363d] px-3 py-1.5 rounded-lg text-cyan-400 font-mono">
            <Cpu className="w-3.5 h-3.5" />
            <span>RAG Engine Online</span>
          </div>
        </div>
      </div>
    </header>
  );
}
