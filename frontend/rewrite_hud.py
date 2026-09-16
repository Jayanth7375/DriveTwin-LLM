import os

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\components\EngineSchematicI6.jsx"

react_code = """import React from 'react';
import { 
  Activity, Flame, ShieldAlert, CheckCircle2, Wind, Droplets,
  Settings, Gauge, ActivitySquare, Zap, Cpu, AlertTriangle
} from 'lucide-react';

export default function EngineSchematicI6({ mlPrediction, physicsSummary }) {
  const faultCode = mlPrediction?.fault_code || "NO_ISSUE";
  const cpi = physicsSummary?.cpi_scores || {};
  
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
    // A dummy sparkline for the UI mockup feel
    return (
      <svg className="w-full h-8 overflow-visible mt-2" viewBox="0 0 100 20">
        <path 
          d="M0,10 Q10,20 20,10 T40,10 T60,15 T80,5 T100,10" 
          fill="none" 
          className={`stroke-current ${colorClass}`}
          strokeWidth="2" 
          strokeLinecap="round" 
        />
        <path 
          d="M0,10 Q10,20 20,10 T40,10 T60,15 T80,5 T100,10" 
          fill="none" 
          className={`stroke-current ${colorClass} opacity-30`}
          strokeWidth="6" 
          strokeLinecap="round" 
          filter="blur(2px)"
        />
      </svg>
    );
  };

  const renderCylSparkline = (val, colorClass) => {
    // Dynamic sparkline based on value
    const path = val < -1.0 
      ? "M0,15 Q10,18 20,12 T40,16 T60,19 T80,10 T100,15" 
      : "M0,10 Q10,5 20,8 T40,12 T60,5 T80,10 T100,8";
    
    return (
      <svg className="w-full h-8 overflow-visible mt-4" viewBox="0 0 100 20">
        <path d={path} fill="none" className={`stroke-current ${colorClass}`} strokeWidth="2" strokeLinecap="round" />
        <path d={path} fill="none" className={`stroke-current ${colorClass} opacity-30`} strokeWidth="6" strokeLinecap="round" filter="blur(2px)" />
      </svg>
    );
  };

  const getStatusColors = (status) => {
    if (status === "FAULT") return { border: "border-red-500/50", bg: "bg-red-500/5", text: "text-red-500", glow: "shadow-[0_0_15px_rgba(239,68,68,0.1)]" };
    if (status === "WARNING") return { border: "border-amber-500/50", bg: "bg-amber-500/5", text: "text-amber-500", glow: "shadow-[0_0_15px_rgba(245,158,11,0.1)]" };
    return { border: "border-emerald-500/20", bg: "bg-emerald-500/5", text: "text-emerald-500", glow: "" };
  };

  return (
    <div className="bg-[#090c10] border border-white/10 rounded-3xl p-6 shadow-2xl text-white space-y-6">
      
      {/* HEADER */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-400">
            4. INLINE-6 VISUAL HUD & CYLINDER MAP
          </h2>
          <p className="text-xs text-gray-400 mt-1">Real-time mechanical diagram with cylinder power indices and key subsystems</p>
        </div>
        
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-3 px-4 py-2 bg-purple-500/10 border border-purple-500/20 rounded-xl">
            <Settings className="w-5 h-5 text-purple-400 animate-spin-slow" />
            <div className="text-right">
              <p className="text-[11px] font-bold text-white">Inline-6 Diesel Engine</p>
              <p className="text-[9px] text-gray-400">Live Telemetry | Digital Twin</p>
            </div>
          </div>
          <div className="px-4 py-3 bg-blue-500/10 border border-blue-500/20 rounded-xl text-xs font-mono font-bold text-blue-400">
            Firing Order: 1 - 5 - 3 - 6 - 2 - 4
          </div>
        </div>
      </div>

      {/* TOP SECTION: ENGINE IMAGE & SCHEMATIC */}
      <div className="grid grid-cols-1 xl:grid-cols-5 gap-6">
        
        {/* Left: 3D Engine Overview */}
        <div className="xl:col-span-2 relative bg-gradient-to-br from-blue-950/40 to-[#090c10] border border-blue-500/20 rounded-2xl overflow-hidden p-6 flex flex-col justify-between min-h-[300px]">
          {/* Subtle glow behind engine */}
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-cyan-500/20 rounded-full blur-[80px] pointer-events-none"></div>
          
          <div className="relative z-10">
            <h3 className="text-lg font-black text-cyan-400 leading-tight">Inline-6</h3>
            <h4 className="text-sm font-bold text-white tracking-widest uppercase mb-4">Diesel Engine</h4>
            
            <ul className="space-y-3 text-xs text-gray-300 font-mono">
              <li className="flex items-center gap-2"><Zap className="w-4 h-4 text-cyan-500" /> Common Rail</li>
              <li className="flex items-center gap-2"><Settings className="w-4 h-4 text-blue-500" /> VGT Turbo</li>
              <li className="flex items-center gap-2"><Wind className="w-4 h-4 text-emerald-500" /> EGR System</li>
              <li className="flex items-center gap-2"><Droplets className="w-4 h-4 text-purple-500" /> HPFP</li>
              <li className="flex items-center gap-2"><ActivitySquare className="w-4 h-4 text-blue-400" /> Intake & Exhaust</li>
            </ul>
          </div>
          
          <img 
            src="/engine-render.jpg" 
            alt="Engine" 
            className="absolute right-[-20%] top-[10%] w-[120%] h-[120%] object-contain opacity-90 mix-blend-screen pointer-events-none drop-shadow-[0_0_30px_rgba(34,211,238,0.2)]"
          />
          
          <p className="relative z-10 text-[10px] text-cyan-500/60 italic mt-8">"Real-Time Visibility for a Healthier Engine"</p>
        </div>

        {/* Right: Interactive SVG Schematic */}
        <div className="xl:col-span-3 bg-white/5 border border-white/10 rounded-2xl p-6 relative">
          <div className="flex items-center gap-2 mb-8">
            <Activity className="w-5 h-5 text-blue-400" />
            <h3 className="text-sm font-bold text-white">Engine Mechanical & Subsystem Schematic</h3>
          </div>
          
          {/* SVG Diagram Container */}
          <div className="relative w-full h-[220px] bg-transparent">
            {/* The SVG lines connecting blocks */}
            <svg className="absolute inset-0 w-full h-full pointer-events-none z-0">
              {/* Intake to Turbo */}
              <path d="M 80 120 L 150 120" stroke="#3b82f6" strokeWidth="2" strokeDasharray="4 2" className="animate-pulse" />
              {/* Turbo to Cylinders (Intake Manifold) */}
              <path d="M 230 120 L 290 120" stroke="#3b82f6" strokeWidth="2" />
              
              {/* Fuel Rail (Red) */}
              <path d="M 310 40 L 550 40" stroke="#ef4444" strokeWidth="4" />
              {/* Injectors (Red lines down) */}
              <path d="M 320 40 L 320 80 M 365 40 L 365 80 M 410 40 L 410 80 M 455 40 L 455 80 M 500 40 L 500 80 M 545 40 L 545 80" stroke="#ef4444" strokeWidth="2" />
              
              {/* Exhaust Manifold (Orange) */}
              <path d="M 320 160 L 320 180 M 365 160 L 365 180 M 410 160 L 410 180 M 455 160 L 455 180 M 500 160 L 500 180 M 545 160 L 545 180" stroke="#f97316" strokeWidth="2" />
              <path d="M 310 180 L 650 180" stroke="#f97316" strokeWidth="4" />
              
              {/* Exhaust Out */}
              <path d="M 730 180 L 780 180" stroke="#f97316" strokeWidth="2" />
              
              {/* EGR Loop (Green) */}
              <path d="M 590 180 L 590 90 L 630 90" stroke="#10b981" strokeWidth="2" />
              <path d="M 690 90 L 730 90 L 730 40 L 550 40" stroke="#10b981" strokeWidth="2" strokeDasharray="4 4" className="animate-pulse" />
            </svg>
            
            {/* HTML Nodes overlaying SVG */}
            <div className="absolute top-[100px] left-0 w-[80px] h-[40px] bg-blue-500/10 border border-blue-500/40 rounded-lg flex items-center justify-center text-[10px] font-bold text-blue-300">
              Air Intake
            </div>
            
            <div className={`absolute top-[90px] left-[150px] w-[80px] h-[60px] rounded-lg border flex flex-col items-center justify-center bg-[#090c10] z-10 ${getSubsystemStatus('TURBO') === 'FAULT' ? 'border-red-500 text-red-500 shadow-[0_0_15px_rgba(239,68,68,0.3)]' : 'border-blue-500/50 text-blue-400 shadow-[0_0_15px_rgba(59,130,246,0.2)]'}`}>
              <Wind className="w-6 h-6 mb-1" />
              <span className="text-[9px] font-bold text-center leading-tight">VGT<br/>Turbocharger</span>
            </div>
            
            {/* Fuel Rail Label */}
            <div className={`absolute top-[15px] left-[400px] -translate-x-1/2 px-3 py-1 rounded-full text-[9px] font-bold border z-10 ${getSubsystemStatus('FUEL_RAIL') === 'FAULT' ? 'bg-red-500/20 border-red-500 text-red-400' : 'bg-red-500/10 border-red-500/30 text-red-300'}`}>
              Common Rail (High Pressure Fuel)
            </div>

            {/* Cylinders Block */}
            <div className="absolute top-[80px] left-[290px] w-[280px] h-[80px] bg-white/5 border border-white/20 rounded-xl flex items-center justify-around px-2 z-10">
              {[1, 2, 3, 4, 5, 6].map(i => {
                const stat = getCylinderStatus(i);
                const isFault = stat === 'FAULT';
                return (
                  <div key={i} className="flex flex-col items-center">
                    <div className={`w-[24px] h-[34px] border-2 border-t-0 rounded-b-md flex items-end justify-center pb-1 ${isFault ? 'border-red-500' : 'border-gray-500'}`}>
                      <div className={`w-[16px] h-[10px] bg-gray-300 rounded-sm flex items-center justify-center ${isFault ? 'bg-red-400' : 'bg-gray-300'}`}>
                        <div className="w-[2px] h-[14px] bg-gray-400 absolute bottom-[10px]"></div>
                      </div>
                    </div>
                    <span className={`text-[10px] font-black mt-2 ${isFault ? 'text-red-500' : 'text-gray-400'}`}>{i}</span>
                  </div>
                );
              })}
              <div className="absolute -bottom-6 text-[9px] text-gray-500 font-mono tracking-widest uppercase">Crankshaft (Centerline Axis)</div>
            </div>

            {/* EGR Valve */}
            <div className={`absolute top-[75px] left-[630px] w-[60px] h-[30px] rounded-lg border flex items-center justify-center bg-[#090c10] z-10 ${getSubsystemStatus('EGR') === 'WARNING' ? 'border-amber-500 text-amber-500 shadow-[0_0_10px_rgba(245,158,11,0.2)]' : 'border-emerald-500/50 text-emerald-400'}`}>
              <span className="text-[10px] font-bold text-center leading-tight">EGR<br/>Valve</span>
            </div>

            {/* Exhaust Manifold */}
            <div className="absolute top-[160px] left-[650px] w-[80px] h-[40px] rounded-lg border border-orange-500/50 bg-[#090c10] flex items-center justify-center z-10">
              <span className="text-[10px] font-bold text-orange-400 text-center leading-tight">Exhaust<br/>Manifold</span>
            </div>
            
            {/* Exhaust Out */}
            <div className="absolute top-[165px] left-[780px] text-[10px] font-bold text-orange-300">
              Exhaust<br/>Out
            </div>
          </div>
        </div>
      </div>

      {/* SENSOR HIGHLIGHTS ROW */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {/* MAF */}
        <div className={`p-4 rounded-2xl border flex items-center justify-between ${getSubsystemStatus('MAF') !== 'OK' ? 'border-amber-500/40 bg-amber-500/5' : 'border-blue-500/20 bg-blue-500/5'}`}>
          <div className="flex items-center gap-3">
            <div className={`w-10 h-10 rounded-full flex items-center justify-center ${getSubsystemStatus('MAF') !== 'OK' ? 'bg-amber-500/20 text-amber-500' : 'bg-blue-500/20 text-blue-400'}`}>
              <Wind className="w-5 h-5" />
            </div>
            <div>
              <p className="text-[11px] font-bold text-gray-400">MAF Sensor</p>
              <h3 className="text-sm font-black text-white">-45.1% <span className="text-[10px] font-normal text-gray-500">residual</span></h3>
            </div>
          </div>
          <div className="w-20">
            {renderSparkline(getSubsystemStatus('MAF') !== 'OK' ? 'text-amber-500' : 'text-blue-500')}
          </div>
        </div>

        {/* Turbo */}
        <div className={`p-4 rounded-2xl border flex items-center justify-between ${getSubsystemStatus('TURBO') !== 'OK' ? 'border-red-500/40 bg-red-500/5' : 'border-cyan-500/20 bg-cyan-500/5'}`}>
          <div className="flex items-center gap-3">
            <div className={`w-10 h-10 rounded-full flex items-center justify-center ${getSubsystemStatus('TURBO') !== 'OK' ? 'bg-red-500/20 text-red-500' : 'bg-cyan-500/20 text-cyan-400'}`}>
              <Settings className="w-5 h-5" />
            </div>
            <div>
              <p className="text-[11px] font-bold text-gray-400">Turbocharger</p>
              <h3 className="text-sm font-black text-white">0.59 <span className="text-[10px] font-normal text-gray-500">bar boost</span></h3>
            </div>
          </div>
          <div className="w-20">
            {renderSparkline(getSubsystemStatus('TURBO') !== 'OK' ? 'text-red-500' : 'text-cyan-500')}
          </div>
        </div>

        {/* EGR */}
        <div className="p-4 rounded-2xl border border-emerald-500/20 bg-emerald-500/5 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center">
              <Activity className="w-5 h-5" />
            </div>
            <div>
              <p className="text-[11px] font-bold text-gray-400">EGR Valve</p>
              <h3 className="text-sm font-black text-white">Recirculation</h3>
            </div>
          </div>
          <div className="w-20">
            {renderSparkline('text-emerald-500')}
          </div>
        </div>

        {/* Fuel Rail */}
        <div className={`p-4 rounded-2xl border flex items-center justify-between ${getSubsystemStatus('FUEL_RAIL') !== 'OK' ? 'border-red-500/40 bg-red-500/5' : 'border-purple-500/20 bg-purple-500/5'}`}>
          <div className="flex items-center gap-3">
            <div className={`w-10 h-10 rounded-full flex items-center justify-center ${getSubsystemStatus('FUEL_RAIL') !== 'OK' ? 'bg-red-500/20 text-red-500' : 'bg-purple-500/20 text-purple-400'}`}>
              <Flame className="w-5 h-5" />
            </div>
            <div>
              <p className="text-[11px] font-bold text-gray-400">Fuel Rail / HPFP</p>
              <h3 className="text-sm font-black text-white">High Pressure</h3>
            </div>
          </div>
          <div className="w-20">
            {renderSparkline(getSubsystemStatus('FUEL_RAIL') !== 'OK' ? 'text-red-500' : 'text-purple-500')}
          </div>
        </div>
      </div>

      {/* CYLINDER POWER INDEX GRID */}
      <div className="bg-white/5 border border-white/10 rounded-2xl p-5">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-2">
            <ActivitySquare className="w-5 h-5 text-blue-400" />
            <h3 className="text-sm font-bold text-white">Cylinder Power Index (Real-Time)</h3>
          </div>
          
          <div className="flex items-center gap-2 text-xs">
            <span className="text-gray-500 mr-2">View:</span>
            <button className="px-3 py-1.5 bg-blue-500/20 text-blue-400 border border-blue-500/30 rounded-lg font-bold">Power Index</button>
            <button className="px-3 py-1.5 text-gray-400 hover:text-white">Compression</button>
            <button className="px-3 py-1.5 text-gray-400 hover:text-white">Combustion</button>
            <button className="px-3 py-1.5 text-gray-400 hover:text-white">Temperature</button>
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {[1, 2, 3, 4, 5, 6].map((i) => {
            const status = getCylinderStatus(i);
            const style = getStatusColors(status);
            const val = cpi[`CPI_Cyl_${i}`] || (status === 'FAULT' ? -2.236 : 0.456);
            
            return (
              <div key={i} className={`p-4 rounded-xl border ${style.border} ${style.bg} ${style.glow} flex flex-col justify-between transition-all duration-300 relative overflow-hidden`}>
                <div className="flex items-center justify-between mb-6 relative z-10">
                  <h4 className="text-xs font-bold text-white">Cylinder {i}</h4>
                  {status === 'FAULT' ? (
                    <div className="flex items-center gap-1 text-[10px] text-red-500 font-bold bg-red-500/10 px-1.5 py-0.5 rounded border border-red-500/20">
                      <AlertTriangle className="w-3 h-3" /> FAULT
                    </div>
                  ) : status === 'WARNING' ? (
                    <div className="flex items-center gap-1 text-[10px] text-amber-500 font-bold bg-amber-500/10 px-1.5 py-0.5 rounded border border-amber-500/20">
                      <AlertTriangle className="w-3 h-3" /> WARN
                    </div>
                  ) : (
                    <div className="flex items-center gap-1 text-[10px] text-emerald-500 font-bold">
                      <CheckCircle2 className="w-3 h-3" /> OK
                    </div>
                  )}
                </div>
                
                {/* Piston Icon Graphic */}
                <div className="mx-auto w-10 h-14 relative z-10 mb-4">
                  <div className="absolute top-0 w-full h-2 bg-gray-500 rounded-t-sm"></div>
                  <div className="absolute top-2 w-full h-[2px] bg-gray-700"></div>
                  <div className={`absolute top-3 left-[10%] w-[80%] h-5 rounded-b-sm flex items-center justify-center text-[7px] font-black ${status === 'FAULT' ? 'bg-red-500/80 text-white' : 'bg-cyan-500/80 text-black'}`}>
                    I-0{i}
                  </div>
                  <div className="absolute top-[32px] left-1/2 -translate-x-1/2 w-[4px] h-[20px] bg-gray-400"></div>
                  <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-[16px] h-[6px] rounded-full border-2 border-gray-400"></div>
                </div>

                <div className="text-center relative z-10">
                  <p className="text-[10px] text-gray-400 mb-1">Power Index</p>
                  <div className="flex items-end justify-between">
                    <span className={`text-lg font-black font-mono leading-none ${style.text}`}>
                      {val > 0 ? '+' : ''}{val.toFixed(3)}
                    </span>
                  </div>
                  <div className="mt-1">
                    {renderCylSparkline(val, style.text)}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
      
      {/* Footer Legend */}
      <div className="flex items-center justify-between text-[10px] text-gray-500 font-mono mt-4 pt-4 border-t border-white/5">
        <div className="flex gap-6">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-emerald-500"></div> Nominal Operation
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-amber-500"></div> Moderate Degradation / Lean
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-red-500"></div> Severe Fault / Isolated Misfire
          </div>
        </div>
        <div>Built with PyTorch PINN | NVIDIA GPU CUDA</div>
      </div>
    </div>
  );
}
"""

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(react_code)

