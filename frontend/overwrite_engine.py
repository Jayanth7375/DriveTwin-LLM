import os

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\components\EngineSchematicI6.jsx"

clean_code = """import React from 'react';
import { 
  Activity, Wind, Droplets, Zap, ShieldAlert, CheckCircle2, AlertTriangle, 
  Settings, Gauge, Box, ArrowRight, PlayCircle, FileText, ChevronRight, ActivitySquare, BarChart3
} from 'lucide-react';

export default function EngineSchematicI6({ mlPrediction, physicsSummary }) {
  const faultCode = mlPrediction?.fault_code || "NO_ISSUE";
  const cpi = physicsSummary?.cpi_scores || {};
  const mafActual = physicsSummary?.maf_actual_mean_gs || 245.6;
  
  const getCylinderStatus = (cylNum) => {
    if (faultCode === "CYL_3_IGNITION_MISFIRE" && cylNum === 3) return "FAULT";
    if (faultCode === "CYL_5_INJECTOR_CLOGGING" && cylNum === 5) return "WARNING";
    if (faultCode === "HEAD_GASKET_BREACH" && (cylNum === 2 || cylNum === 3)) return "FAULT";
    const cpiVal = cpi[`CPI_Cyl_${cylNum}`];
    if (cpiVal !== undefined) {
      if (cpiVal < -1.5) return "FAULT";
      if (cpiVal < -0.8) return "WARNING";
    }
    return "OK";
  };

  const getSubsystemStatus = (subsysKey) => {
    if (faultCode === "TURBO_BOOST_LEAK" && subsysKey === "TURBO") return "FAULT";
    if (faultCode === "MAF_SENSOR_DRIFT" && subsysKey === "MAF") return "WARNING";
    if (faultCode === "EGR_VALVE_STUCK_OPEN" && subsysKey === "EGR") return "WARNING";
    if (faultCode === "HPFP_PRESSURE_DROP" && subsysKey === "FUEL_RAIL") return "FAULT";
    return "OK";
  };

  const renderSparkline = (colorClass) => {
    return (
      <svg className="w-full h-8 overflow-visible mt-1" viewBox="0 0 100 20">
        <path 
          d="M0,15 Q10,10 20,15 T40,10 T60,18 T80,8 T100,12" 
          fill="none" 
          className={`stroke-current ${colorClass}`}
          strokeWidth="2.5" 
          strokeLinecap="round" 
        />
      </svg>
    );
  };
  
  const renderFaultSparkline = () => {
    return (
      <svg className="w-full h-8 overflow-visible mt-1" viewBox="0 0 100 20">
        <path 
          d="M0,15 L15,14 L25,18 L35,2 L45,17 L60,16 L80,18 L100,14" 
          fill="none" 
          className="stroke-red-500"
          strokeWidth="2.5" 
          strokeLinecap="round" 
          strokeLinejoin="round"
        />
      </svg>
    );
  };

  return (
    <div className="flex flex-col gap-6 animate-in fade-in duration-500">
      
      {/* TOP ROW: Engine Image Card & Schematic */}
      <div className="grid grid-cols-1 xl:grid-cols-12 gap-6">
        
        {/* Engine Render Card (Left) */}
        <div className="xl:col-span-5 bg-gradient-to-br from-[#f1f5fa] to-white dark:from-[#0d1117] dark:to-[#161b22] rounded-3xl border border-gray-200 dark:border-white/5 p-8 shadow-sm flex flex-col relative overflow-hidden">
          {/* Background Glow */}
          <div className="absolute top-1/2 -right-20 w-96 h-96 bg-blue-100/50 dark:bg-blue-500/10 rounded-full blur-[80px]"></div>
          
          <div className="relative z-10">
            <h3 className="text-xs font-bold text-gray-500 tracking-wider uppercase mb-1">INLINE-6</h3>
            <h1 className="text-4xl font-black text-slate-900 dark:text-white mb-2">Diesel Engine</h1>
            <p className="text-sm text-slate-500 max-w-[200px] mb-8">Real-time insights for maximum performance.</p>
            
            <div className="space-y-4">
              {[
                { icon: <Zap className="w-4 h-4"/>, label: "Common Rail" },
                { icon: <Activity className="w-4 h-4"/>, label: "VGT Turbocharger" },
                { icon: <Settings className="w-4 h-4"/>, label: "EGR System" },
                { icon: <Droplets className="w-4 h-4"/>, label: "HPFP" },
                { icon: <Wind className="w-4 h-4"/>, label: "Intake & Exhaust" }
              ].map((item, i) => (
                <div key={i} className="flex items-center gap-3 text-sm text-slate-600 dark:text-gray-300">
                  <div className="w-8 h-8 rounded-full bg-white dark:bg-white/5 border border-gray-100 dark:border-white/10 flex items-center justify-center shadow-sm">
                    {item.icon}
                  </div>
                  <span className="font-medium">{item.label}</span>
                </div>
              ))}
            </div>
            
            <div className="mt-8 pt-4 border-t border-gray-200 dark:border-white/10 flex items-center gap-2 text-xs text-slate-400">
              <div className="w-4 h-[1px] bg-slate-300"></div>
              <span>Smarter Diagnostics. Stronger Engines.</span>
            </div>
          </div>
          
          {/* Engine Image floating on right */}
          <img 
            src="/engine-render.jpg" 
            alt="3D Engine" 
            className="absolute top-1/2 -translate-y-1/2 -right-20 w-[120%] max-w-[450px] mix-blend-multiply dark:invert-0 invert dark:mix-blend-screen opacity-90 scale-125 origin-right"
            style={{ maskImage: 'radial-gradient(circle at center, black 40%, transparent 70%)', WebkitMaskImage: 'radial-gradient(circle at center, black 40%, transparent 70%)' }}
          />
        </div>
        
        {/* Schematic Card (Right) */}
        <div className="xl:col-span-7 bg-white dark:bg-[#161b22] rounded-3xl border border-gray-200 dark:border-white/5 p-8 shadow-sm flex flex-col relative overflow-hidden">
          <div className="flex items-center justify-between mb-8 relative z-10">
            <div className="flex items-center gap-2">
              <Box className="w-5 h-5 text-slate-700 dark:text-gray-300" />
              <h2 className="font-bold text-slate-900 dark:text-white">Engine Schematic</h2>
            </div>
            <div className="flex bg-slate-100 dark:bg-black/20 rounded-full p-1 border border-slate-200 dark:border-white/5 text-xs font-bold">
              <button className="px-4 py-1.5 rounded-full text-slate-500 hover:text-slate-700">2D</button>
              <button className="px-4 py-1.5 rounded-full bg-slate-800 text-white shadow-sm">3D</button>
            </div>
          </div>
          
          <div className="flex-1 flex items-center justify-center relative min-h-[300px]">
            {/* Extremely custom simplified SVG schematic to mimic the beautiful mockup lines */}
            <svg viewBox="0 0 800 400" className="w-full h-full max-h-[350px]">
              {/* Legends */}
              <g className="text-[10px] font-medium fill-slate-400">
                <line x1="700" y1="50" x2="730" y2="50" stroke="#fb923c" strokeWidth="2" strokeDasharray="4 2"/>
                <text x="740" y="53">High Pressure Fuel</text>
                <line x1="700" y1="70" x2="730" y2="70" stroke="#60a5fa" strokeWidth="2" />
                <text x="740" y="73">Intake Air</text>
                <line x1="700" y1="90" x2="730" y2="90" stroke="#f43f5e" strokeWidth="2" />
                <text x="740" y="93">Exhaust Gas</text>
                <line x1="700" y1="110" x2="730" y2="110" stroke="#4ade80" strokeWidth="2" strokeDasharray="4 2"/>
                <text x="740" y="113">EGR Flow</text>
              </g>

              {/* Main Engine Block Background */}
              <rect x="250" y="120" width="360" height="180" rx="20" fill="none" stroke="#e2e8f0" strokeWidth="6" />
              <rect x="260" y="130" width="340" height="150" rx="15" fill="#f8fafc" className="dark:fill-[#0d1117]" />
              
              {/* Cylinders */}
              {[1, 2, 3, 4, 5, 6].map((c, i) => (
                <g key={i} transform={`translate(${280 + i * 55}, 150)`}>
                  <rect x="0" y="0" width="30" height="80" rx="4" fill="none" stroke="#cbd5e1" strokeWidth="2" />
                  {/* Fire/Piston Effect */}
                  {getCylinderStatus(c) === "FAULT" ? (
                    <rect x="2" y="40" width="26" height="38" rx="2" fill="url(#fireGradient)" />
                  ) : (
                    <rect x="2" y="50" width="26" height="28" rx="2" fill="url(#warmGradient)" className="opacity-80" />
                  )}
                  {/* Injector Line coming from top */}
                  <line x1="15" y1="0" x2="15" y2="-40" stroke="#fb923c" strokeWidth="2" />
                  <text x="15" y="105" textAnchor="middle" className="text-xs font-bold fill-slate-700 dark:fill-white">{c}</text>
                </g>
              ))}

              {/* Gradients */}
              <defs>
                <linearGradient id="fireGradient" x1="0" y1="1" x2="0" y2="0">
                  <stop offset="0%" stopColor="#ef4444" />
                  <stop offset="100%" stopColor="#fef08a" />
                </linearGradient>
                <linearGradient id="warmGradient" x1="0" y1="1" x2="0" y2="0">
                  <stop offset="0%" stopColor="#f97316" />
                  <stop offset="100%" stopColor="#fde047" />
                </linearGradient>
              </defs>

              {/* Common Rail */}
              <rect x="270" y="70" width="340" height="20" rx="10" fill="#fee2e2" stroke="#fca5a5" strokeWidth="2" />
              <text x="440" y="83" textAnchor="middle" className="text-[10px] font-bold fill-red-800">Common Rail (High Pressure Fuel)</text>

              {/* Intake Line from Turbo */}
              <path d="M 180 160 L 250 160" fill="none" stroke="#60a5fa" strokeWidth="3" />
              <path d="M 180 160 L 180 200 L 250 200" fill="none" stroke="#60a5fa" strokeWidth="3" opacity="0.3" />
              
              {/* VGT Turbo Box */}
              <rect x="120" y="140" width="60" height="70" rx="8" fill="#f0f9ff" stroke="#bae6fd" strokeWidth="2" />
              <circle cx="150" cy="165" r="10" fill="none" stroke="#0ea5e9" strokeWidth="2" />
              <path d="M 145 160 L 155 170 M 155 160 L 145 170 M 150 155 L 150 175 M 140 165 L 160 165" stroke="#0ea5e9" strokeWidth="1.5" />
              <text x="150" y="195" textAnchor="middle" className="text-[9px] font-bold fill-slate-700">VGT</text>
              <text x="150" y="205" textAnchor="middle" className="text-[8px] fill-slate-500">Turbocharger</text>

              {/* Air Intake Box */}
              <rect x="20" y="155" width="70" height="40" rx="6" fill="#eff6ff" stroke="#bfdbfe" strokeWidth="2" />
              <text x="55" y="178" textAnchor="middle" className="text-[10px] font-bold fill-blue-700">Air Intake</text>
              <path d="M 90 175 L 120 175" fill="none" stroke="#60a5fa" strokeWidth="3" markerEnd="url(#arrowBlue)" />

              {/* Exhaust Manifold Line */}
              <path d="M 610 220 L 650 220 L 650 250" fill="none" stroke="#f43f5e" strokeWidth="3" />
              
              {/* Exhaust Box */}
              <rect x="620" y="250" width="80" height="50" rx="8" fill="#fff1f2" stroke="#fecdd3" strokeWidth="2" />
              <text x="660" y="275" textAnchor="middle" className="text-[10px] font-bold fill-rose-700">Exhaust</text>
              <text x="660" y="287" textAnchor="middle" className="text-[10px] font-bold fill-rose-700">Manifold</text>

              {/* EGR Line returning to Intake */}
              <path d="M 610 160 L 650 160" fill="none" stroke="#4ade80" strokeWidth="3" strokeDasharray="4 4" />
              <rect x="630" y="130" width="70" height="40" rx="6" fill="#f0fdf4" stroke="#bbf7d0" strokeWidth="2" />
              <circle cx="645" cy="150" r="4" fill="#22c55e" />
              <text x="670" y="147" textAnchor="middle" className="text-[10px] font-bold fill-green-700">EGR</text>
              <text x="670" y="159" textAnchor="middle" className="text-[10px] font-bold fill-green-700">Valve</text>

              {/* Markers */}
              <defs>
                <marker id="arrowBlue" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
                  <path d="M 0 0 L 6 3 L 0 6 z" fill="#60a5fa" />
                </marker>
              </defs>
            </svg>
          </div>
        </div>
      </div>

      {/* MIDDLE ROW: 5 Subsystem KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-5 gap-4">
        {[
          { label: "MAF Sensor", value: "245.6", unit: "kg/h", delta: "+2.4%", trend: "up", icon: <Wind/>, color: "blue", status: getSubsystemStatus("MAF") },
          { label: "Turbocharger", value: "0.59", unit: "bar boost", delta: "+0.03", trend: "up", icon: <Settings/>, color: "blue", status: getSubsystemStatus("TURBO") },
          { label: "EGR Valve", value: "32.4", unit: "% open", delta: "+1.2%", trend: "up", icon: <ActivitySquare/>, color: "green", status: getSubsystemStatus("EGR") },
          { label: "Fuel Rail / HPFP", value: "1,782", unit: "bar", delta: "+12 bar", trend: "up", icon: <Droplets/>, color: "purple", status: getSubsystemStatus("FUEL_RAIL") },
          { label: "Engine Status", value: faultCode === "NO_ISSUE" ? "NORMAL" : "ALERT", unit: faultCode === "NO_ISSUE" ? "All Systems Operational" : faultCode, delta: null, trend: null, icon: <Activity/>, color: faultCode === "NO_ISSUE" ? "green" : "red", status: faultCode === "NO_ISSUE" ? "OK" : "FAULT" }
        ].map((kpi, i) => (
          <div key={i} className={`bg-white dark:bg-[#161b22] border border-gray-100 dark:border-white/5 rounded-2xl p-5 shadow-sm flex flex-col justify-between hover:shadow-md transition-shadow`}>
            <div className="flex items-center gap-3 mb-4">
              <div className={`w-10 h-10 rounded-full flex items-center justify-center bg-${kpi.color}-50 dark:bg-${kpi.color}-500/10 text-${kpi.color}-500`}>
                {kpi.icon}
              </div>
              <div className="flex-1">
                <h4 className="text-xs font-bold text-slate-500">{kpi.label}</h4>
                <div className="flex items-baseline gap-1">
                  <span className={`text-xl font-black ${kpi.status === "FAULT" ? "text-red-500" : "text-slate-800 dark:text-white"}`}>{kpi.value}</span>
                  <span className="text-[10px] text-slate-400">{kpi.unit}</span>
                </div>
              </div>
            </div>
            {kpi.delta ? (
              <div className="flex items-center justify-between text-xs font-bold">
                <span className={kpi.status === "FAULT" ? "text-red-500" : "text-emerald-500"}>▲ {kpi.delta}</span>
                <div className="w-16">
                  {renderSparkline(kpi.status === "FAULT" ? "text-red-500" : `text-${kpi.color}-500`)}
                </div>
              </div>
            ) : (
              <div className="flex items-center justify-between text-xs font-bold mt-auto h-8">
                <span className={kpi.status === "FAULT" ? "text-red-500" : "text-emerald-500"}>{kpi.status}</span>
                <div className="w-16">
                   {renderSparkline(kpi.status === "FAULT" ? "text-red-500" : "text-emerald-500")}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* CPI GRID ROW */}
      <div className="bg-white dark:bg-[#161b22] border border-gray-100 dark:border-white/5 rounded-3xl p-6 shadow-sm">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-blue-500" />
            <h3 className="font-bold text-slate-800 dark:text-white">Cylinder Power Index (Real-Time)</h3>
          </div>
          <div className="hidden md:flex bg-slate-50 dark:bg-[#0d1117] rounded-full p-1 border border-slate-100 dark:border-white/5 text-xs font-medium text-slate-500">
            <button className="px-4 py-1.5 rounded-full bg-blue-500 text-white shadow-sm">Power Index</button>
            <button className="px-4 py-1.5 rounded-full hover:text-slate-700">Compression</button>
            <button className="px-4 py-1.5 rounded-full hover:text-slate-700">Combustion</button>
            <button className="px-4 py-1.5 rounded-full hover:text-slate-700">Temperature</button>
          </div>
        </div>

        <div className="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
          {[1, 2, 3, 4, 5, 6].map(cyl => {
            const status = getCylinderStatus(cyl);
            const val = (cpi[`CPI_Cyl_${cyl}`] || (cyl === 3 && faultCode !== "NO_ISSUE" ? -2.236 : 0.430 + (cyl*0.01))).toFixed(3);
            
            return (
              <div key={cyl} className={`border rounded-2xl p-4 flex flex-col justify-between ${
                status === "FAULT" 
                  ? "bg-red-50/50 dark:bg-red-500/5 border-red-200 dark:border-red-500/20" 
                  : "bg-white dark:bg-[#0d1117] border-gray-100 dark:border-white/5 hover:border-blue-200"
              }`}>
                <div className="flex items-center justify-between mb-3">
                  <span className="text-xs font-bold text-slate-700 dark:text-gray-200">Cylinder {cyl}</span>
                  <div className="flex items-center gap-1 text-[9px] font-bold uppercase tracking-wider">
                    {status === "FAULT" ? (
                      <><span className="w-1.5 h-1.5 rounded-full bg-red-500 animate-pulse"></span> <span className="text-red-500">FAULT</span></>
                    ) : (
                      <><span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span> <span className="text-emerald-500">OK</span></>
                    )}
                  </div>
                </div>
                <div className={`text-2xl font-black tracking-tight mb-2 ${
                  status === "FAULT" ? "text-red-500" : "text-emerald-500"
                }`}>
                  {val > 0 ? "+" : ""}{val}
                </div>
                <div className="w-full">
                  {status === "FAULT" ? renderFaultSparkline() : renderSparkline("text-emerald-500")}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* BOTTOM ROW: Health, Alerts, Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Overall Health */}
        <div className="bg-white dark:bg-[#161b22] border border-gray-100 dark:border-white/5 rounded-3xl p-6 shadow-sm flex flex-col">
          <div className="flex items-center gap-2 mb-6">
            <ShieldAlert className="w-5 h-5 text-blue-500" />
            <h3 className="font-bold text-slate-800 dark:text-white">Overall Engine Health</h3>
          </div>
          <div className="flex items-center justify-between flex-1">
            <div className="relative w-32 h-32 flex items-center justify-center">
              <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="40" stroke="currentColor" strokeWidth="8" fill="none" className="text-slate-100 dark:text-gray-800" />
                <circle cx="50" cy="50" r="40" stroke="currentColor" strokeWidth="8" fill="none" strokeDasharray="251.2" strokeDashoffset={251.2 * (1 - (faultCode === "NO_ISSUE" ? 0.98 : 0.83))} className={faultCode === "NO_ISSUE" ? "text-emerald-500" : "text-emerald-400"} />
              </svg>
              <div className="absolute flex flex-col items-center">
                <span className="text-2xl font-black text-slate-800 dark:text-white">{faultCode === "NO_ISSUE" ? "98%" : "83%"}</span>
                <span className="text-[9px] font-bold text-emerald-500 uppercase">{faultCode === "NO_ISSUE" ? "Excellent" : "Good Condition"}</span>
              </div>
            </div>
            <div className="space-y-3">
              {[
                { label: "Combustion Stable", ok: faultCode !== "CYL_3_IGNITION_MISFIRE" },
                { label: "Fuel System Normal", ok: true },
                { label: "Air Intake Optimal", ok: faultCode !== "MAF_SENSOR_DRIFT" },
                { label: "Emissions Within Limit", ok: true }
              ].map((item, i) => (
                <div key={i} className="flex items-center gap-2 text-xs font-medium text-slate-600 dark:text-gray-300">
                  <CheckCircle2 className={`w-3.5 h-3.5 ${item.ok ? 'text-emerald-500' : 'text-red-500'}`} />
                  {item.label}
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Recent Alerts */}
        <div className="bg-white dark:bg-[#161b22] border border-gray-100 dark:border-white/5 rounded-3xl p-6 shadow-sm flex flex-col">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-slate-700 dark:text-gray-300" />
              <h3 className="font-bold text-slate-800 dark:text-white">Recent Alerts</h3>
            </div>
            <span className="text-xs font-bold text-blue-500 cursor-pointer">View All</span>
          </div>
          <div className="space-y-3 flex-1 overflow-y-auto">
            {faultCode !== "NO_ISSUE" && (
              <div className="flex items-center justify-between p-3 rounded-xl bg-slate-50 dark:bg-[#0d1117] border border-slate-100 dark:border-white/5">
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 rounded-full bg-red-500"></div>
                  <span className="text-xs font-medium text-slate-700 dark:text-gray-200">Cylinder 3 Power Index Low</span>
                </div>
                <span className="text-[10px] text-slate-400">09:41 PM</span>
              </div>
            )}
            {faultCode !== "NO_ISSUE" && (
              <div className="flex items-center justify-between p-3 rounded-xl bg-slate-50 dark:bg-[#0d1117] border border-slate-100 dark:border-white/5">
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 rounded-full bg-amber-500"></div>
                  <span className="text-xs font-medium text-slate-700 dark:text-gray-200">Check Combustion / Injector</span>
                </div>
                <span className="text-[10px] text-slate-400">09:41 PM</span>
              </div>
            )}
            <div className="flex items-center justify-between p-3 rounded-xl bg-slate-50 dark:bg-[#0d1117] border border-slate-100 dark:border-white/5">
              <div className="flex items-center gap-3">
                <div className="w-2 h-2 rounded-full bg-emerald-500"></div>
                <span className="text-xs font-medium text-slate-700 dark:text-gray-200">All Other Cylinders Normal</span>
              </div>
              <span className="text-[10px] text-slate-400">09:40 PM</span>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white dark:bg-[#161b22] border border-gray-100 dark:border-white/5 rounded-3xl p-6 shadow-sm flex flex-col">
          <div className="flex items-center gap-2 mb-6">
            <Zap className="w-5 h-5 text-slate-700 dark:text-gray-300" />
            <h3 className="font-bold text-slate-800 dark:text-white">Quick Actions</h3>
          </div>
          <div className="grid grid-cols-2 gap-3 flex-1">
            <button className="flex items-center justify-center gap-2 bg-slate-800 hover:bg-slate-700 text-white rounded-xl p-3 text-xs font-bold transition-colors">
              <PlayCircle className="w-4 h-4" /> Run Diagnostics
            </button>
            <button className="flex items-center justify-center gap-2 bg-slate-50 hover:bg-slate-100 dark:bg-white/5 dark:hover:bg-white/10 text-slate-700 dark:text-gray-200 border border-slate-200 dark:border-white/10 rounded-xl p-3 text-xs font-bold transition-colors">
              <FileText className="w-4 h-4" /> Generate Report
            </button>
            <button className="flex items-center justify-center gap-2 bg-slate-50 hover:bg-slate-100 dark:bg-white/5 dark:hover:bg-white/10 text-slate-700 dark:text-gray-200 border border-slate-200 dark:border-white/10 rounded-xl p-3 text-xs font-bold transition-colors">
              <Gauge className="w-4 h-4" /> Calibrate Sensors
            </button>
            <button className="flex items-center justify-center gap-2 bg-slate-50 hover:bg-slate-100 dark:bg-white/5 dark:hover:bg-white/10 text-slate-700 dark:text-gray-200 border border-slate-200 dark:border-white/10 rounded-xl p-3 text-xs font-bold transition-colors">
              <Box className="w-4 h-4" /> View 3D Model
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}
"""

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(clean_code)

