import React from 'react';
import { 
  FileSpreadsheet, 
  Activity, 
  BarChart3, 
  Sparkles, 
  MessageSquare, 
  Gauge, 
  Box
} from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab, hardwareInfo }) {
  const navItems = [
    { id: 'overview', label: 'Diagnostics Overview', icon: FileSpreadsheet, badge: 'Main' },
    { id: 'llm', label: 'RAG LLM Repair Report', icon: Sparkles, badge: 'AI Report' },
    { id: 'digitaltwin', label: '3D Engine Digital Twin', icon: Box, badge: '3D WebGL' },
    { id: 'schematic', label: 'Engine Visual HUD', icon: Activity, badge: 'Interactive' },
    { id: 'physics', label: 'Physics & PINN Metrics', icon: BarChart3, badge: 'PyTorch' },
    { id: 'chat', label: 'Mechanic AI Chat', icon: MessageSquare, badge: 'Q&A' },
  ];

  return (
    <aside className="w-64 bg-[#161b22] border-r border-[#30363d] flex flex-col justify-between h-screen sticky top-0 shrink-0 select-none shadow-xl z-50 rounded-none">
      <div>
        {/* Top App Branding */}
        <div className="p-4 border-b border-[#30363d] flex items-center gap-3 bg-[#0d1117]/50 rounded-none">
          <div className="p-2 bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 shrink-0 rounded-none">
            <Gauge className="w-6 h-6 animate-pulse" />
          </div>
          <div>
            <h1 className="text-sm font-bold tracking-wide text-white leading-tight">
              DIESEL I6 ENGINE
            </h1>
            <p className="text-[10px] text-cyan-400 font-mono font-semibold">
              LLM Diagnostic Suite
            </p>
          </div>
        </div>

        {/* Vertical Navigation Items */}
        <nav className="p-3 space-y-1 mt-2 rounded-none">
          <div className="text-[10px] font-bold text-gray-500 px-3 mb-1 uppercase tracking-wider">
            Diagnostic Modules
          </div>
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center justify-between px-3 py-2.5 text-xs font-semibold transition-all rounded-none ${
                  isActive
                    ? 'bg-cyan-600 text-white shadow-md border border-cyan-400'
                    : 'text-gray-400 hover:text-white hover:bg-[#21262d]'
                }`}
              >
                <div className="flex items-center gap-2.5">
                  <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-cyan-400'}`} />
                  <span>{item.label}</span>
                </div>
                {item.badge && (
                  <span className={`text-[9px] font-mono px-1.5 py-0.5 rounded-none ${
                    isActive
                      ? 'bg-white/20 text-white'
                      : 'bg-[#0d1117] text-gray-400 border border-[#30363d]'
                  }`}>
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Footer Branding */}
      <div className="p-4 border-t border-[#30363d] bg-[#0d1117]/50 text-center text-[10px] font-mono text-gray-500 rounded-none">
        Diesel I6 Diagnostic Suite v1.0
      </div>
    </aside>
  );
}
