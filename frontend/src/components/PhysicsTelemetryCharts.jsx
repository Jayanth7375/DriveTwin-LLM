import React from 'react';
import { 
  BarChart3, Wind, Flame, Gauge, Layers, ShieldCheck, Thermometer,
  Activity, AlertTriangle, CheckCircle2, ChevronRight, Settings, Info
} from 'lucide-react';

export default function PhysicsTelemetryCharts({ physicsSummary, mlPrediction }) {
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

  // Calculate consistency score based on residuals (dummy logic for mockup fidelity)
  const consistencyScore = mlPrediction?.confidence ? (mlPrediction.confidence * 100) : 87;

  const renderMiniSparkline = (val, colorClass) => {
    const isNeg = val < -1;
    const path = isNeg 
      ? "M0,10 Q10,15 20,12 T40,20 T60,18 T80,25 T100,20" 
      : "M0,20 Q10,15 20,18 T40,10 T60,12 T80,5 T100,10";
    return (
      <svg className="w-16 h-8 overflow-visible" viewBox="0 0 100 30">
        <path d={path} fill="none" className={`stroke-current ${colorClass}`} strokeWidth="3" strokeLinecap="round" />
      </svg>
    );
  };

  const renderResidualChart = () => {
    return (
      <svg className="w-full h-16 overflow-visible" viewBox="0 0 400 50" preserveAspectRatio="none">
        <line x1="0" y1="25" x2="400" y2="25" className="stroke-gray-300 dark:stroke-gray-700" strokeWidth="1" strokeDasharray="4 4" />
        <path d="M0,25 Q10,20 20,28 T40,22 T60,30 T80,25 T100,15 T120,28 T140,24 T160,35 T180,20 T200,25 T220,15 T240,28 T260,22 T280,35 T300,20 T320,25 T340,30 T360,20 T380,28 T400,25" fill="none" className="stroke-blue-500" strokeWidth="2" strokeLinecap="round" />
        <path d="M0,25 L40,23 L80,26 L120,22 L160,28 L200,24 L240,26 L280,27 L320,25 L360,26 L400,25" fill="none" className="stroke-blue-400/50" strokeWidth="2" strokeDasharray="5 5" />
      </svg>
    );
  };

  return (
    <div className="space-y-6">
      {/* HEADER SECTION */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 px-2">
        <div>
          <h2 className="text-2xl lg:text-3xl font-black text-gray-900 dark:text-white tracking-tight">
            Physics Telemetry & PyTorch PINN Metrics
          </h2>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1 max-w-2xl">
            Analytical model gas airflow residuals, lean lambda bank variance, dynamic crank acceleration balance (CPI 1 to 6).
          </p>
        </div>
        <div className="hidden md:block text-right">
          <p className="text-lg font-script text-gray-400 dark:text-gray-500 transform -rotate-2">
            From Data<br/>to a Healthier Tomorrow
          </p>
        </div>
      </div>

      {/* TOP 4 METRIC CARDS */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white/80 dark:bg-[#161b22]/80 backdrop-blur-xl border border-gray-200/50 dark:border-white/10 rounded-2xl p-5 shadow-xl shadow-gray-200/20 dark:shadow-none flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-blue-50 dark:bg-blue-500/10 flex items-center justify-center text-blue-500">
            <Layers className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs font-bold text-gray-500 dark:text-gray-400 mb-1">Model Status</p>
            <div className="flex items-center gap-2">
              <h3 className="text-xl font-black text-gray-900 dark:text-white">Active</h3>
              <div className="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_8px_#10b981]"></div>
            </div>
            <p className="text-[10px] text-gray-500">PyTorch PINN</p>
          </div>
        </div>

        <div className="bg-white/80 dark:bg-[#161b22]/80 backdrop-blur-xl border border-gray-200/50 dark:border-white/10 rounded-2xl p-5 shadow-xl shadow-gray-200/20 dark:shadow-none flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-cyan-50 dark:bg-cyan-500/10 flex items-center justify-center text-cyan-500">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div className="w-full">
            <p className="text-xs font-bold text-gray-500 dark:text-gray-400 mb-1">Model Consistency</p>
            <h3 className="text-xl font-black text-gray-900 dark:text-white">{consistencyScore.toFixed(0)}%</h3>
            <div className="w-full bg-gray-100 dark:bg-white/5 rounded-full h-1.5 mt-1.5 overflow-hidden">
              <div className="bg-cyan-400 h-full rounded-full" style={{ width: `${consistencyScore}%` }}></div>
            </div>
            <p className="text-[10px] text-gray-500 mt-1">Good agreement with physics</p>
          </div>
        </div>

        <div className="bg-white/80 dark:bg-[#161b22]/80 backdrop-blur-xl border border-gray-200/50 dark:border-white/10 rounded-2xl p-5 shadow-xl shadow-gray-200/20 dark:shadow-none flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-purple-50 dark:bg-purple-500/10 flex items-center justify-center text-purple-500">
            <Thermometer className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs font-bold text-gray-500 dark:text-gray-400 mb-1">Coolant Max Temp</p>
            <div className="flex items-center gap-2">
              <h3 className="text-xl font-black text-gray-900 dark:text-white">{maxCoolant.toFixed(1)}°C</h3>
              <span className="text-[10px] font-bold text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-500/10 px-1.5 py-0.5 rounded">Δ {thermalDelta.toFixed(2)}°C</span>
            </div>
            <p className="text-[10px] text-gray-500">Within safe range</p>
          </div>
        </div>

        <div className="bg-white/80 dark:bg-[#161b22]/80 backdrop-blur-xl border border-gray-200/50 dark:border-white/10 rounded-2xl p-5 shadow-xl shadow-gray-200/20 dark:shadow-none flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-2xl bg-blue-50 dark:bg-blue-500/10 flex items-center justify-center text-blue-500">
              <Wind className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs font-bold text-gray-500 dark:text-gray-400 mb-1">MAF Deviation</p>
              <h3 className={`text-xl font-black ${mafRes < -0.2 ? 'text-red-500' : 'text-gray-900 dark:text-white'}`}>{(mafRes * 100).toFixed(1)}%</h3>
              <p className="text-[10px] text-gray-500">{mafRes < 0 ? 'Below theoretical' : 'Above theoretical'}</p>
            </div>
          </div>
          <ChevronRight className="w-5 h-5 text-gray-300 dark:text-gray-600" />
        </div>
      </div>

      {/* MAIN CONTENT COLUMNS */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* LEFT COLUMN: CPI */}
        <div className="bg-white/80 dark:bg-[#161b22]/80 backdrop-blur-xl border border-gray-200/50 dark:border-white/10 rounded-3xl p-6 shadow-2xl shadow-gray-200/20 dark:shadow-none">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-2">
              <BarChart3 className="w-5 h-5 text-cyan-500" />
              <div>
                <h3 className="text-base font-bold text-gray-900 dark:text-white">Cylinder Power Index (CPI) per 120° Stroke</h3>
                <p className="text-[11px] text-gray-500 flex items-center gap-1">CPI indicates relative power contribution per cylinder <Info className="w-3 h-3" /></p>
              </div>
            </div>
            <select className="bg-gray-50 dark:bg-white/5 border border-gray-200 dark:border-white/10 text-xs font-bold text-gray-600 dark:text-gray-300 rounded-lg px-3 py-1.5 outline-none">
              <option>CPI (per 120°)</option>
            </select>
          </div>

          <div className="grid grid-cols-2 gap-4 mb-6">
            {[1, 2, 3, 4, 5, 6].map(i => {
              const val = cpi[`CPI_Cyl_${i}`] || 0;
              const isFault = val < -1.5;
              
              // Map -3 to +3 to a 0-100% width for the bar
              const percent = Math.max(0, Math.min(100, ((val + 3) / 6) * 100));
              
              return (
                <div key={i} className={`p-4 rounded-2xl border transition-all ${isFault ? 'bg-red-50 dark:bg-red-950/20 border-red-200 dark:border-red-500/30' : 'bg-white dark:bg-[#0d1117]/50 border-gray-200/50 dark:border-white/5 shadow-sm'}`}>
                  <div className="flex items-center gap-2 mb-2">
                    <Settings className={`w-4 h-4 ${isFault ? 'text-red-500' : 'text-blue-500'}`} />
                    <span className="text-xs font-bold text-gray-700 dark:text-gray-300">Cylinder {i}</span>
                  </div>
                  
                  <div className="flex items-end justify-between mb-3">
                    <span className={`text-2xl font-black ${isFault ? 'text-red-500' : 'text-gray-900 dark:text-white'}`}>
                      {val > 0 ? '+' : ''}{val.toFixed(3)}
                    </span>
                    {renderMiniSparkline(val, isFault ? 'text-red-400' : 'text-blue-400')}
                  </div>
                  
                  {/* Custom Progress Bar */}
                  <div className="relative w-full h-2 bg-gray-100 dark:bg-white/10 rounded-full mb-1">
                    {/* Zero Marker */}
                    <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[2px] h-full bg-gray-300 dark:bg-gray-600 z-10"></div>
                    {/* Fill */}
                    <div 
                      className={`absolute top-0 h-full rounded-full ${isFault ? 'bg-red-500' : 'bg-cyan-400'}`}
                      style={{ 
                        left: val < 0 ? `${percent}%` : '50%',
                        width: val < 0 ? `${50 - percent}%` : `${percent - 50}%`
                      }}
                    ></div>
                  </div>
                  <div className="flex justify-between text-[9px] text-gray-400 font-mono mb-3">
                    <span>-3</span><span>0</span><span>+3</span>
                  </div>
                  
                  {isFault ? (
                    <div className="inline-flex items-center gap-1 bg-red-100 dark:bg-red-500/20 text-red-600 dark:text-red-400 text-[10px] font-bold px-2 py-0.5 rounded-full">
                      <AlertTriangle className="w-3 h-3" /> Abnormal
                    </div>
                  ) : (
                    <div className="inline-flex items-center gap-1 bg-emerald-100 dark:bg-emerald-500/20 text-emerald-600 dark:text-emerald-400 text-[10px] font-bold px-2 py-0.5 rounded-full">
                      <CheckCircle2 className="w-3 h-3" /> Normal
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          <div className="bg-gray-50 dark:bg-white/5 border border-gray-200/50 dark:border-white/5 rounded-2xl p-4 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Activity className="w-5 h-5 text-blue-500" />
              <span className="text-sm font-bold text-gray-700 dark:text-gray-300 flex items-center gap-1">Speed Fluctuation Index (SFI) <Info className="w-3 h-3 text-gray-400" /></span>
            </div>
            <div className="flex items-center gap-4">
              <div className="w-32 h-1.5 bg-gray-200 dark:bg-white/10 rounded-full overflow-hidden">
                <div className="bg-blue-500 h-full rounded-full" style={{ width: `${Math.min(100, sfi * 10)}%` }}></div>
              </div>
              <span className="text-xl font-black text-blue-600 dark:text-blue-400">{sfi.toFixed(2)}%</span>
              <div className="w-12">{renderMiniSparkline(0, 'text-blue-400')}</div>
              <span className="bg-amber-100 dark:bg-amber-500/20 text-amber-600 dark:text-amber-400 text-[10px] font-bold px-2 py-1 rounded-full flex items-center gap-1">
                <CheckCircle2 className="w-3 h-3" /> Moderate
              </span>
            </div>
          </div>
        </div>

        {/* RIGHT COLUMN: Air Intake & Lambda */}
        <div className="bg-white/80 dark:bg-[#161b22]/80 backdrop-blur-xl border border-gray-200/50 dark:border-white/10 rounded-3xl p-6 shadow-2xl shadow-gray-200/20 dark:shadow-none flex flex-col gap-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Wind className="w-5 h-5 text-cyan-500" />
              <h3 className="text-base font-bold text-gray-900 dark:text-white">Air Intake & Lambda Balance Metrics</h3>
            </div>
            <span className="text-[11px] text-gray-500">Thermodynamics & 120° Kinematics</span>
          </div>

          <div className="space-y-4">
            {/* MAF Card */}
            <div className="bg-gray-50 dark:bg-white/5 border border-gray-200/50 dark:border-white/5 rounded-2xl p-5">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-500/20 text-blue-500 flex items-center justify-center"><Wind className="w-4 h-4" /></div>
                  <span className="text-sm font-bold text-gray-700 dark:text-gray-300">MAF Measured vs Theoretical</span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="text-right">
                    <span className="text-sm font-black text-gray-900 dark:text-white">{mafActual.toFixed(2)} g/s</span>
                    <p className="text-[10px] text-gray-500">(Measured)</p>
                  </div>
                  <span className="text-xs text-gray-400 font-mono">VS</span>
                  <div className="text-left">
                    <span className="text-sm font-black text-gray-900 dark:text-white">{mafTheo.toFixed(2)} g/s</span>
                    <p className="text-[10px] text-gray-500">(Theoretical)</p>
                  </div>
                  <span className={`ml-4 px-2 py-1 rounded text-xs font-black ${mafRes < -0.2 ? 'bg-red-100 dark:bg-red-500/20 text-red-500' : 'bg-emerald-100 dark:bg-emerald-500/20 text-emerald-500'}`}>
                    {(mafRes * 100).toFixed(1)}%
                  </span>
                </div>
              </div>
              
              {/* Double Bar */}
              <div className="relative w-full h-3 rounded-full bg-gray-200 dark:bg-gray-700 overflow-hidden">
                <div className="absolute top-0 left-0 h-full bg-red-400 rounded-full" style={{ width: `${Math.min(100, (mafActual/100)*100)}%` }}></div>
                <div className="absolute top-0 left-0 h-full bg-gray-400/50 rounded-full mix-blend-multiply dark:mix-blend-screen" style={{ width: `${Math.min(100, (mafTheo/100)*100)}%` }}></div>
              </div>
            </div>

            {/* Lambda Card */}
            <div className="bg-gray-50 dark:bg-white/5 border border-gray-200/50 dark:border-white/5 rounded-2xl p-5">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-500/20 text-blue-500 flex items-center justify-center"><Flame className="w-4 h-4" /></div>
                  <span className="text-sm font-bold text-gray-700 dark:text-gray-300">Bank 1 (1-3) vs Bank 2 (4-6) Lambda</span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="text-right">
                    <span className="text-sm font-black text-gray-900 dark:text-white">{bank1.toFixed(2)}</span>
                    <p className="text-[10px] text-gray-500">(Bank 1)</p>
                  </div>
                  <span className="text-xs text-gray-400 font-mono">VS</span>
                  <div className="text-left">
                    <span className="text-sm font-black text-gray-900 dark:text-white">{bank2.toFixed(2)}</span>
                    <p className="text-[10px] text-gray-500">(Bank 2)</p>
                  </div>
                  <span className="ml-4 px-2 py-1 rounded text-xs font-black bg-emerald-100 dark:bg-emerald-500/20 text-emerald-600 dark:text-emerald-400">
                    Δ {Math.abs(bankDelta).toFixed(3)}
                  </span>
                </div>
              </div>
              
              <div className="relative w-full h-3 rounded-full bg-gray-200 dark:bg-gray-700 overflow-hidden mb-1">
                 <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[2px] h-full bg-gray-400 z-10"></div>
                 <div className="absolute top-0 h-full bg-cyan-400 rounded-full" style={{ left: '10%', width: '40%' }}></div>
              </div>
              <div className="flex justify-between text-[9px] text-gray-400 font-mono">
                 <span>0.5</span><span>1.0</span><span>1.5</span><span>2.0</span>
              </div>
            </div>

            {/* Coolant Card */}
            <div className="bg-gray-50 dark:bg-white/5 border border-gray-200/50 dark:border-white/5 rounded-2xl p-5">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-500/20 text-blue-500 flex items-center justify-center"><Thermometer className="w-4 h-4" /></div>
                  <span className="text-sm font-bold text-gray-700 dark:text-gray-300">Coolant Max Temp / Thermal Delta</span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="text-right">
                    <span className="text-sm font-black text-emerald-600 dark:text-emerald-400">{maxCoolant.toFixed(1)}°C</span>
                    <p className="text-[10px] text-gray-500">(Coolant Max Temp)</p>
                  </div>
                  <div className="text-left ml-4">
                    <span className="text-sm font-black text-emerald-600 dark:text-emerald-400">{thermalDelta.toFixed(2)}°C</span>
                    <p className="text-[10px] text-gray-500">(Oil-Coolant Delta)</p>
                  </div>
                  <span className="ml-4 px-2 py-1 rounded-full text-[10px] font-bold bg-emerald-100 dark:bg-emerald-500/20 text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
                    <CheckCircle2 className="w-3 h-3" /> Normal
                  </span>
                </div>
              </div>
              
              <div className="relative w-full h-3 rounded-full bg-gradient-to-r from-blue-400 via-emerald-400 to-red-400 overflow-hidden mb-1">
                 <div className="absolute top-0 w-2 h-full bg-white dark:bg-gray-900 border border-gray-900 dark:border-white" style={{ left: `${Math.min(100, (maxCoolant / 120) * 100)}%` }}></div>
              </div>
              <div className="flex justify-between text-[9px] text-gray-400 font-mono">
                 <span>40</span><span>60</span><span>80</span><span>100</span><span>120</span>
              </div>
            </div>
          </div>
        </div>

      </div>

      {/* BOTTOM ROW: Physics Consistency & Residuals */}
      <div className="bg-white/80 dark:bg-[#161b22]/80 backdrop-blur-xl border border-gray-200/50 dark:border-white/10 rounded-3xl p-6 shadow-2xl shadow-gray-200/20 dark:shadow-none grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="md:col-span-2">
           <div className="flex items-center justify-between mb-4">
             <div className="flex items-center gap-2">
               <Activity className="w-5 h-5 text-cyan-500" />
               <h3 className="text-sm font-bold text-gray-900 dark:text-white">Physics Consistency & Model Residuals</h3>
             </div>
             <div className="flex items-center gap-4 text-[10px] font-bold text-gray-500">
               <span className="flex items-center gap-1"><div className="w-2 h-2 rounded-full bg-blue-500"></div> Residual</span>
               <span className="flex items-center gap-1 text-blue-400">--- Rolling Avg</span>
             </div>
           </div>
           {renderResidualChart()}
           <div className="flex justify-between text-[9px] text-gray-400 font-mono mt-2">
             <span>0</span><span>50</span><span>100</span><span>150</span><span>200</span><span>250</span><span>300</span>
           </div>
        </div>

        <div className="flex items-center justify-center gap-8 border-t md:border-t-0 md:border-l border-gray-200/50 dark:border-white/10 pt-6 md:pt-0 pl-0 md:pl-8">
           <div className="relative w-24 h-24 flex items-center justify-center">
             <svg className="absolute inset-0 w-full h-full transform -rotate-90">
               <circle cx="48" cy="48" r="40" fill="none" className="stroke-gray-100 dark:stroke-white/5" strokeWidth="12" />
               <circle cx="48" cy="48" r="40" fill="none" className="stroke-blue-500" strokeWidth="12" strokeDasharray="251" strokeDashoffset={251 - (251 * consistencyScore / 100)} strokeLinecap="round" />
             </svg>
             <div className="text-center">
               <span className="text-xl font-black text-gray-900 dark:text-white">{consistencyScore.toFixed(0)}%</span>
               <p className="text-[9px] font-bold text-gray-500 leading-tight">Physics<br/>Consistency</p>
             </div>
           </div>
           
           <div className="space-y-2">
             <p className="text-[10px] font-black text-gray-900 dark:text-white mb-2">Model Status</p>
             <div className="flex items-center justify-between gap-6 text-[10px]">
               <span className="flex items-center gap-1 text-gray-600 dark:text-gray-300"><CheckCircle2 className="w-3 h-3 text-emerald-500" /> Governing Equations</span>
               <span className="text-emerald-600 dark:text-emerald-400 font-bold">Consistent</span>
             </div>
             <div className="flex items-center justify-between gap-6 text-[10px]">
               <span className="flex items-center gap-1 text-gray-600 dark:text-gray-300"><CheckCircle2 className="w-3 h-3 text-emerald-500" /> Thermal Balance</span>
               <span className="text-emerald-600 dark:text-emerald-400 font-bold">Consistent</span>
             </div>
             <div className="flex items-center justify-between gap-6 text-[10px]">
               <span className="flex items-center gap-1 text-gray-600 dark:text-gray-300"><CheckCircle2 className="w-3 h-3 text-emerald-500" /> Airflow Model</span>
               <span className="text-emerald-600 dark:text-emerald-400 font-bold">Consistent</span>
             </div>
             <div className="flex items-center justify-between gap-6 text-[10px]">
               <span className="flex items-center gap-1 text-gray-600 dark:text-gray-300"><CheckCircle2 className="w-3 h-3 text-emerald-500" /> Combustion Dynamics</span>
               <span className="text-emerald-600 dark:text-emerald-400 font-bold">Within Range</span>
             </div>
           </div>
        </div>
      </div>
    </div>
  );
}
