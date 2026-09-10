import React from 'react';
import { BarChart3, Wind, Flame, Gauge, Layers } from 'lucide-react';

export default function PhysicsTelemetryCharts({ physicsSummary }) {
  if (!physicsSummary) return null;

  const cpi = physicsSummary.cpi_scores || {};
  const mafActual = physicsSummary.maf_actual_mean_gs || 0;
  const mafTheo = physicsSummary.maf_theoretical_mean_gs || 0;
  const mafRes = physicsSummary.maf_residual_ratio || 0;
  const bank1 = physicsSummary.lambda_bank1_mean || 1.0;
  const bank2 = physicsSummary.lambda_bank2_mean || 1.0;
  const bankDelta = physicsSummary.lambda_bank_delta || 0.0;
  const sfi = physicsSummary.speed_fluctuation_index_pct || 0.0;
  const maxCoolant = physicsSummary.max_coolant_temp_c || 90.0;
  const thermalDelta = physicsSummary.thermal_delta_c || 5.0;

  return (
    <div className="bg-[#161b22] border border-[#30363d] rounded-xl p-5 shadow-sm">
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-[#30363d]">
        <h2 className="text-base font-semibold text-white flex items-center gap-2">
          <BarChart3 className="w-5 h-5 text-cyan-400" />
          Physics-Based Metrics & Thermodynamic Residuals
        </h2>
        <span className="text-xs text-gray-400">Thermodynamics & 120° Kinematics</span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* CPI Cylinder Power Index Table */}
        <div className="bg-[#0d1117] border border-[#30363d] rounded-xl p-4">
          <h3 className="text-xs font-semibold text-gray-300 mb-3 flex items-center gap-1.5">
            <Layers className="w-3.5 h-3.5 text-cyan-400" />
            Cylinder Power Index (CPI) per 120° Stroke
          </h3>
          <div className="grid grid-cols-3 gap-2 text-center text-xs">
            {[1, 2, 3, 4, 5, 6].map((cyl) => {
              const val = cpi[`CPI_Cyl_${cyl}`] ?? 0.0;
              const isBad = val < -1.5;
              const isWarn = val < -0.8;
              return (
                <div key={cyl} className={`p-2 rounded border ${
                  isBad
                    ? "border-red-500/50 bg-red-950/30 text-red-300"
                    : isWarn
                    ? "border-amber-500/50 bg-amber-950/30 text-amber-300"
                    : "border-[#30363d] bg-[#161b22] text-gray-200"
                }`}>
                  <div className="text-[10px] text-gray-400">Cylinder {cyl}</div>
                  <div className="font-mono font-bold text-sm mt-0.5">
                    {val > 0 ? `+${val}` : val}
                  </div>
                </div>
              );
            })}
          </div>
          <div className="mt-3 text-[11px] text-gray-400 flex items-center justify-between">
            <span>Speed Fluctuation Index (SFI):</span>
            <span className="font-mono font-bold text-cyan-300">{sfi}%</span>
          </div>
        </div>

        {/* Airflow & Lambda Metrics */}
        <div className="bg-[#0d1117] border border-[#30363d] rounded-xl p-4 flex flex-col justify-between">
          <div>
            <h3 className="text-xs font-semibold text-gray-300 mb-3 flex items-center gap-1.5">
              <Wind className="w-3.5 h-3.5 text-cyan-400" />
              Air Intake & Lambda Balance Metrics
            </h3>

            <div className="space-y-2 text-xs">
              <div className="flex justify-between items-center bg-[#161b22] p-2 rounded border border-[#30363d]">
                <span className="text-gray-400">MAF Measured vs Theoretical:</span>
                <span className="font-mono font-semibold text-white">
                  {mafActual} g/s vs {mafTheo} g/s ({mafRes >= 0 ? `+${(mafRes*100).toFixed(1)}%` : `${(mafRes*100).toFixed(1)}%`})
                </span>
              </div>

              <div className="flex justify-between items-center bg-[#161b22] p-2 rounded border border-[#30363d]">
                <span className="text-gray-400">Bank 1 (1-3) vs Bank 2 (4-6) Lambda:</span>
                <span className="font-mono font-semibold text-white">
                  {bank1} vs {bank2} (Δ {bankDelta})
                </span>
              </div>

              <div className="flex justify-between items-center bg-[#161b22] p-2 rounded border border-[#30363d]">
                <span className="text-gray-400">Coolant Max Temp / Thermal Delta:</span>
                <span className={`font-mono font-semibold ${maxCoolant > 105 ? "text-red-400" : "text-emerald-400"}`}>
                  {maxCoolant}°C (Oil-Coolant Δ {thermalDelta}°C)
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
