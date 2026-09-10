import React from 'react';
import { Activity, Flame, ShieldAlert, CheckCircle2, Wind, Droplets } from 'lucide-react';

export default function EngineSchematicI6({ mlPrediction, physicsSummary }) {
  const faultCode = mlPrediction?.fault_code || "NO_ISSUE";
  const isolatedLoc = mlPrediction?.isolated_location || "";
  const cpi = physicsSummary?.cpi_scores || {};
  
  // Helper to determine status color per cylinder
  const getCylinderStatus = (cylNum) => {
    if (faultCode === "CYL_3_IGNITION_MISFIRE" && cylNum === 3) return "FAULT";
    if (faultCode === "CYL_5_INJECTOR_CLOGGING" && cylNum === 5) return "WARNING";
    if (faultCode === "HEAD_GASKET_BREACH" && (cylNum === 2 || cylNum === 3)) return "FAULT";
    
    // CPI threshold check
    const cpiVal = cpi[`CPI_Cyl_${cylNum}`];
    if (cpiVal !== undefined) {
      if (cpiVal < -2.0) return "FAULT";
      if (cpiVal < -1.0) return "WARNING";
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

  return (
    <div className="bg-[#161b22] border border-[#30363d] rounded-xl p-5 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-base font-semibold text-white flex items-center gap-2">
          <Activity className="w-5 h-5 text-cyan-400" />
          Inline-6 Engine Mechanical & Subsystem Schematic
        </h2>
        <span className="text-xs font-mono text-cyan-400 bg-cyan-500/10 px-2.5 py-1 rounded border border-cyan-500/30">
          Firing Order: 1 - 5 - 3 - 6 - 2 - 4
        </span>
      </div>

      {/* Engine Graphic Container */}
      <div className="bg-[#0d1117] border border-[#30363d] rounded-xl p-5 relative overflow-hidden">
        {/* Top Header Labels for Bank 1 (1-3) & Bank 2 (4-6) */}
        <div className="flex justify-between items-center text-xs font-mono mb-4 px-2">
          <div className="bg-blue-500/10 border border-blue-500/30 px-3 py-1 rounded text-blue-400">
            BANK 1: Cylinders 1, 2, 3
          </div>
          <div className="text-gray-500 text-[10px]">Crankshaft Centerline Axis</div>
          <div className="bg-purple-500/10 border border-purple-500/30 px-3 py-1 rounded text-purple-400">
            BANK 2: Cylinders 4, 5, 6
          </div>
        </div>

        {/* Auxiliary Subsystems Row (MAF, Turbo, Intercooler, EGR, HPFP) */}
        <div className="grid grid-cols-4 gap-2 mb-5">
          <div className={`p-2.5 rounded-lg border text-center transition-all ${
            getSubsystemStatus("MAF") === "WARNING"
              ? "border-amber-500/50 bg-amber-500/10 text-amber-300"
              : "border-[#30363d] bg-[#161b22] text-gray-300"
          }`}>
            <Wind className="w-4 h-4 mx-auto mb-1 text-cyan-400" />
            <div className="text-[11px] font-semibold">MAF Sensor</div>
            <div className="text-[10px] opacity-75">{physicsSummary?.maf_residual_ratio ? `${(physicsSummary.maf_residual_ratio*100).toFixed(1)}% residual` : "Nominal"}</div>
          </div>

          <div className={`p-2.5 rounded-lg border text-center transition-all ${
            getSubsystemStatus("TURBO") === "FAULT"
              ? "border-red-500/50 bg-red-500/10 text-red-300 animate-pulse"
              : "border-[#30363d] bg-[#161b22] text-gray-300"
          }`}>
            <Activity className="w-4 h-4 mx-auto mb-1 text-cyan-400" />
            <div className="text-[11px] font-semibold">Turbocharger</div>
            <div className="text-[10px] opacity-75">{physicsSummary?.boost_pressure_max_bar ? `${physicsSummary.boost_pressure_max_bar} bar boost` : "Active"}</div>
          </div>

          <div className={`p-2.5 rounded-lg border text-center transition-all ${
            getSubsystemStatus("EGR") === "WARNING"
              ? "border-amber-500/50 bg-amber-500/10 text-amber-300"
              : "border-[#30363d] bg-[#161b22] text-gray-300"
          }`}>
            <Wind className="w-4 h-4 mx-auto mb-1 text-emerald-400" />
            <div className="text-[11px] font-semibold">EGR Valve</div>
            <div className="text-[10px] opacity-75">Recirculation</div>
          </div>

          <div className={`p-2.5 rounded-lg border text-center transition-all ${
            getSubsystemStatus("FUEL_RAIL") === "FAULT"
              ? "border-red-500/50 bg-red-500/10 text-red-300 animate-pulse"
              : "border-[#30363d] bg-[#161b22] text-gray-300"
          }`}>
            <Droplets className="w-4 h-4 mx-auto mb-1 text-cyan-400" />
            <div className="text-[11px] font-semibold">Fuel Rail / HPFP</div>
            <div className="text-[10px] opacity-75">High Pressure</div>
          </div>
        </div>

        {/* 6 Cylinders Array Graphic */}
        <div className="grid grid-cols-6 gap-3">
          {[1, 2, 3, 4, 5, 6].map((cylNum) => {
            const status = getCylinderStatus(cylNum);
            const cpiVal = cpi[`CPI_Cyl_${cylNum}`] ?? 0.0;
            const isBank1 = cylNum <= 3;

            return (
              <div
                key={cylNum}
                className={`relative p-3 rounded-xl border flex flex-col items-center justify-between transition-all ${
                  status === "FAULT"
                    ? "border-red-500 bg-red-950/30 text-white shadow-lg shadow-red-500/10 animate-pulse"
                    : status === "WARNING"
                    ? "border-amber-500 bg-amber-950/20 text-white shadow-lg shadow-amber-500/10"
                    : "border-[#30363d] bg-[#161b22] text-gray-300 hover:border-gray-500"
                }`}
              >
                {/* Cylinder Header Badge */}
                <div className="flex items-center justify-between w-full text-[10px] font-mono mb-2">
                  <span className={`px-1.5 py-0.5 rounded font-bold ${isBank1 ? "bg-blue-500/20 text-blue-300" : "bg-purple-500/20 text-purple-300"}`}>
                    CYL {cylNum}
                  </span>
                  {status === "FAULT" && <ShieldAlert className="w-3.5 h-3.5 text-red-400" />}
                  {status === "WARNING" && <Flame className="w-3.5 h-3.5 text-amber-400" />}
                  {status === "OK" && <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />}
                </div>

                {/* Cylinder Piston Visual SVG */}
                <div className="w-12 h-14 border border-current rounded-lg my-1.5 flex flex-col items-center justify-center relative overflow-hidden bg-black/40">
                  <div className={`w-10 h-3 rounded-t border-b ${status === "FAULT" ? "bg-red-500" : status === "WARNING" ? "bg-amber-500" : "bg-cyan-500"}`} />
                  <div className="w-1.5 h-6 bg-gray-500 my-0.5" />
                  <div className="text-[9px] font-mono opacity-80 mt-auto pb-0.5">
                    {status}
                  </div>
                </div>

                {/* CPI Score */}
                <div className="w-full text-center mt-1 pt-1.5 border-t border-current/20 text-[10px] font-mono">
                  <div className="text-gray-400 text-[9px]">Power Index</div>
                  <div className={`font-bold ${cpiVal < -1.5 ? "text-red-400" : cpiVal < -0.8 ? "text-amber-400" : "text-emerald-400"}`}>
                    {cpiVal > 0 ? `+${cpiVal}` : cpiVal}
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Legend Footer */}
        <div className="mt-4 flex items-center justify-center gap-6 text-xs text-gray-400 border-t border-[#30363d] pt-3">
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
            <span>Nominal Operation</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-amber-500" />
            <span>Moderate Degradation / Lean</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-red-500 animate-pulse" />
            <span>Severe Fault / Isolated Misfire</span>
          </div>
        </div>
      </div>
    </div>
  );
}
