import React, { useState, useEffect } from 'react';
import { 
  Activity, 
  Gauge, 
  Wind, 
  Flame, 
  Droplets, 
  Zap, 
  ShieldAlert, 
  CheckCircle2, 
  TrendingUp,
  LineChart,
  Play,
  Pause,
  RotateCcw,
  Clock
} from 'lucide-react';

export default function LiveTelemetrySheet({ telemetryPreview, latestSensors, physicsSummary, mlPrediction }) {
  const [history, setHistory] = useState([]);
  const [playbackIndex, setPlaybackIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(true);
  const [speedMs, setSpeedMs] = useState(80); // 80ms per frame for smooth 12.5 Hz playback

  // When a new file or dataset scenario is loaded, reset playback to start
  useEffect(() => {
    if (telemetryPreview && telemetryPreview.length > 0) {
      setPlaybackIndex(0);
      setIsPlaying(true);
      setHistory([telemetryPreview[0]]);
    }
  }, [telemetryPreview]);

  // Automated timestamp playback timer loop
  useEffect(() => {
    let timer = null;
    if (isPlaying && telemetryPreview && telemetryPreview.length > 0) {
      timer = setInterval(() => {
        setPlaybackIndex((prev) => {
          if (prev < telemetryPreview.length - 1) {
            const nextIdx = prev + 1;
            const currentItem = telemetryPreview[nextIdx];
            setHistory((prevHist) => [...prevHist, currentItem].slice(-30));
            return nextIdx;
          } else {
            // Reached end of timeline
            setIsPlaying(false);
            return prev;
          }
        });
      }, speedMs);
    }
    return () => {
      if (timer) clearInterval(timer);
    };
  }, [isPlaying, telemetryPreview, speedMs]);

  // Fallback sensor values when static or starting
  const currentSensors = (telemetryPreview && telemetryPreview.length > 0)
    ? telemetryPreview[playbackIndex]
    : latestSensors;

  const cpi = physicsSummary?.cpi_scores || {};
  const faultCode = mlPrediction?.fault_code || "NO_ISSUE";

  const getSensorStatus = (key) => {
    if (faultCode === "CYL_3_IGNITION_MISFIRE" && key === "Crank_Accel_C3") return "FAULT";
    if (faultCode === "CYL_5_INJECTOR_CLOGGING" && key === "Crank_Accel_C5") return "WARNING";
    if (faultCode === "TURBO_BOOST_LEAK" && (key === "Boost_Pressure" || key === "MAF")) return "FAULT";
    if (faultCode === "MAF_SENSOR_DRIFT" && key === "MAF") return "WARNING";
    if (faultCode === "HEAD_GASKET_BREACH" && key === "Coolant_Temp") return "FAULT";
    if (faultCode === "HPFP_PRESSURE_DROP" && (key === "Lambda_B1" || key === "Lambda_B2")) return "FAULT";
    return "NOMINAL";
  };

  const sensorCards = [
    { key: "RPM", name: "Engine Speed", unit: "RPM", icon: Gauge, color: "text-cyan-400" },
    { key: "MAP", name: "Manifold Pressure (MAP)", unit: "kPa", icon: Wind, color: "text-cyan-400" },
    { key: "MAF", name: "Mass Air Flow (MAF)", unit: "g/s", icon: Wind, color: "text-cyan-400" },
    { key: "Boost_Pressure", name: "VGT Boost Pressure", unit: "kPa", icon: Activity, color: "text-cyan-400" },
    { key: "Wastegate_Duty", name: "Wastegate Duty Cycle", unit: "%", icon: Zap, color: "text-cyan-400" },
    { key: "Lambda_B1", name: "Bank 1 Diesel Lambda", unit: "Ratio", icon: Droplets, color: "text-emerald-400" },
    { key: "Lambda_B2", name: "Bank 2 Diesel Lambda", unit: "Ratio", icon: Droplets, color: "text-emerald-400" },
    { key: "Coolant_Temp", name: "Coolant Temperature", unit: "┬░C", icon: Flame, color: "text-amber-400" },
    { key: "Oil_Temp", name: "Oil Temperature", unit: "┬░C", icon: Flame, color: "text-amber-400" },
    { key: "Crank_Accel_C1", name: "Cylinder 1 Acceleration", unit: "rad/s┬▓", icon: TrendingUp, color: "text-cyan-400" },
    { key: "Crank_Accel_C2", name: "Cylinder 2 Acceleration", unit: "rad/s┬▓", icon: TrendingUp, color: "text-cyan-400" },
    { key: "Crank_Accel_C3", name: "Cylinder 3 Acceleration", unit: "rad/s┬▓", icon: TrendingUp, color: "text-cyan-400" },
    { key: "Crank_Accel_C4", name: "Cylinder 4 Acceleration", unit: "rad/s┬▓", icon: TrendingUp, color: "text-cyan-400" },
    { key: "Crank_Accel_C5", name: "Cylinder 5 Acceleration", unit: "rad/s┬▓", icon: TrendingUp, color: "text-cyan-400" },
    { key: "Crank_Accel_C6", name: "Cylinder 6 Acceleration", unit: "rad/s┬▓", icon: TrendingUp, color: "text-cyan-400" },
  ];

  // Renders a smooth animated SVG mini sparkline for a given sensor key
  const renderSparkline = (key, strokeColor = "#38bdf8") => {
    if (!history || history.length < 2) return null;
    
    const values = history.map((h) => {
      if (h && h[key] !== undefined) return h[key];
      if (key.startsWith("Crank_Accel_C")) {
        const cyl = key.replace("Crank_Accel_C", "");
        return cpi[`Mean_Accel_Cyl_${cyl}`] ?? 18.0;
      }
      return 0;
    });

    const min = Math.min(...values);
    const max = Math.max(...values);
    const range = (max - min) || 1;
    
    const width = 120;
    const height = 30;

    const points = values.map((val, idx) => {
      const x = (idx / (values.length - 1)) * width;
      const y = height - ((val - min) / range) * (height - 6) - 3;
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    }).join(" ");

    return (
      <svg width={width} height={height} className="overflow-visible">
        <polyline
          fill="none"
          stroke={strokeColor}
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          points={points}
        />
      </svg>
    );
  };

  const totalRows = telemetryPreview ? telemetryPreview.length : 1;
  const progressPercent = Math.round(((playbackIndex + 1) / totalRows) * 100);
  const currentTime = currentSensors?.Time_s !== undefined 
    ? `${currentSensors.Time_s.toFixed(1)}s`
    : `${(playbackIndex * 0.1).toFixed(1)}s`;
  const totalTime = (telemetryPreview && telemetryPreview.length > 0 && telemetryPreview[telemetryPreview.length - 1]?.Time_s)
    ? `${telemetryPreview[telemetryPreview.length - 1].Time_s.toFixed(1)}s`
    : `${(totalRows * 0.1).toFixed(1)}s`;

  return (
    <div className="bg-white/60 dark:bg-[#161b22]/60 backdrop-blur-xl border border-gray-200/50 dark:border-white/10 rounded-3xl p-6 shadow-2xl shadow-black/5 dark:shadow-black/40 ring-1 ring-black/5 dark:ring-white/5 transition-all duration-300 space-y-5">
      {/* Header Banner & Playback Stream Controls */}
      <div className="flex flex-col md:flex-row md:items-center justify-between border-b border-gray-200/50 dark:border-white/10 pb-3 gap-3">
        <div className="flex items-center gap-2">
          <LineChart className="w-5 h-5 text-cyan-400" />
          <div>
            <h3 className="text-sm font-bold bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-500 dark:from-white dark:to-gray-400 uppercase tracking-wider font-mono">
              Live ECU Telemetry Sensor Grid & Dynamic Oscilloscope
            </h3>
            <span className="text-[11px] text-gray-500 dark:text-gray-400 font-mono">
              Dynamic Row-by-Row Playback from Telemetry Log ΓÇó Timestamp Stream
            </span>
          </div>
        </div>

        {/* Live Playback Controls */}
        <div className="flex items-center gap-2 text-xs font-mono">
          <button
            onClick={() => setIsPlaying(!isPlaying)}
            className="px-3 py-1.5 bg-gradient-to-r from-emerald-500 to-emerald-600 hover:from-emerald-400 hover:to-emerald-500 shadow-lg hover:shadow-emerald-500/25 hover:-translate-y-0.5 border-transparent text-white font-bold flex items-center gap-1.5 transition-colors border border-cyan-400 rounded-2xl shadow"
          >
            {isPlaying ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
            <span>{isPlaying ? 'PAUSE STREAM' : 'PLAY LIVE'}</span>
          </button>

          <button
            onClick={() => {
              setPlaybackIndex(0);
              setIsPlaying(true);
              if (telemetryPreview && telemetryPreview[0]) setHistory([telemetryPreview[0]]);
            }}
            className="p-1.5 bg-[#0d1117] hover:bg-gray-800 text-gray-600 dark:text-gray-300 border border-gray-200/50 dark:border-white/10 transition-colors rounded-2xl"
            title="Replay Telemetry Stream"
          >
            <RotateCcw className="w-3.5 h-3.5" />
          </button>

          <div className="flex items-center bg-white/40 dark:bg-[#0d1117]/40 backdrop-blur-md border border-gray-200/50 dark:border-white/5 hover:border-gray-300/50 dark:hover:border-white/10 transition-colors duration-300 border-gray-200/50 dark:border-white/10 px-2 py-1 text-[11px] text-cyan-300 gap-1 rounded-2xl">
            <Clock className="w-3.5 h-3.5 text-cyan-400" />
            <span>{currentTime} / {totalTime}</span>
          </div>

          <select
            value={speedMs}
            onChange={(e) => setSpeedMs(Number(e.target.value))}
            className="bg-white/40 dark:bg-[#0d1117]/40 backdrop-blur-md border border-gray-200/50 dark:border-white/5 hover:border-gray-300/50 dark:hover:border-white/10 transition-colors duration-300 border-gray-200/50 dark:border-white/10 px-2 py-1 text-[11px] text-gray-700 dark:text-gray-200 font-mono focus:outline-none focus:border-cyan-400 rounded-2xl"
          >
            <option value={150}>0.5x Speed</option>
            <option value={80}>1x Normal</option>
            <option value={30}>3x Fast</option>
            <option value={10}>Max Speed</option>
          </select>

          <span className={`px-2.5 py-1 flex items-center gap-1.5 rounded-2xl font-bold border ${
            isPlaying 
              ? 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30 animate-pulse' 
              : 'text-amber-400 bg-amber-500/10 border-amber-500/30'
          }`}>
            <Activity className="w-3.5 h-3.5" />
            <span>{isPlaying ? 'STREAMING' : 'PAUSED'}</span>
          </span>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="w-full bg-[#0d1117] h-1.5 border border-gray-200/50 dark:border-white/10 overflow-hidden relative">
        <div 
          className="bg-cyan-500 h-full transition-all duration-75"
          style={{ width: `${progressPercent}%` }}
        />
      </div>

      {/* Top Oscilloscope Moving Waveform Banner */}
      <div className="bg-white/40 dark:bg-[#0d1117]/40 backdrop-blur-md border border-gray-200/50 dark:border-white/5 hover:border-gray-300/50 dark:hover:border-white/10 transition-colors duration-300 border-gray-200/50 dark:border-white/10 p-4 rounded-2xl space-y-2">
        <div className="flex items-center justify-between text-xs font-mono">
          <span className="text-cyan-400 font-bold flex items-center gap-1.5">
            <TrendingUp className="w-4 h-4 text-cyan-400" />
            Multi-Channel Telemetry Waveform Oscilloscope (RPM & Air Intake Dynamics)
          </span>
          <span className="text-gray-500 dark:text-gray-400 text-[10px]">Rolling 30-Point Signal Window ({progressPercent}% Completed)</span>
        </div>

        <div className="h-16 w-full flex items-center justify-center bg-black/40 border border-gray-200/50 dark:border-white/10 p-2 overflow-hidden relative">
          <div className="absolute inset-0 bg-grid-pattern opacity-10" />
          <div className="w-full flex items-center justify-between">
            <div className="space-y-1">
              <span className="text-[10px] text-gray-500 dark:text-gray-400 font-mono block">Engine Speed Signal (RPM)</span>
              {renderSparkline("RPM", "#38bdf8")}
            </div>
            <div className="space-y-1">
              <span className="text-[10px] text-gray-500 dark:text-gray-400 font-mono block">VGT Boost Pressure (kPa)</span>
              {renderSparkline("Boost_Pressure", "#34d399")}
            </div>
            <div className="space-y-1">
              <span className="text-[10px] text-gray-500 dark:text-gray-400 font-mono block">Cylinder 3 Acceleration</span>
              {renderSparkline("Crank_Accel_C3", "#f87171")}
            </div>
          </div>
        </div>
      </div>

      {/* 4x4 Telemetry Sensor Grid Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
        {sensorCards.map((s) => {
          const Icon = s.icon;
          const status = getSensorStatus(s.key);
          const rawVal = currentSensors ? currentSensors[s.key] : null;
          
          let displayVal = "--";
          if (rawVal !== null && rawVal !== undefined) {
            displayVal = typeof rawVal === 'number' ? rawVal.toFixed(s.unit === 'Ratio' ? 3 : 1) : rawVal;
          } else if (s.key.startsWith("Crank_Accel_C")) {
            const cylNum = s.key.replace("Crank_Accel_C", "");
            const cpiVal = cpi[`Mean_Accel_Cyl_${cylNum}`] ?? 18.0;
            displayVal = cpiVal.toFixed(1);
          } else if (s.key === "RPM") displayVal = "2,145.0";
          else if (s.key === "MAP") displayVal = "184.2";
          else if (s.key === "MAF") displayVal = "28.4";
          else if (s.key === "Boost_Pressure") displayVal = "82.9";
          else if (s.key === "Wastegate_Duty") displayVal = "48.1";
          else if (s.key === "Lambda_B1") displayVal = "1.345";
          else if (s.key === "Lambda_B2") displayVal = "1.348";
          else if (s.key === "Coolant_Temp") displayVal = "92.4";
          else if (s.key === "Oil_Temp") displayVal = "96.8";

          const sparklineColor = status === "FAULT" ? "#f87171" : status === "WARNING" ? "#fbbf24" : "#38bdf8";

          return (
            <div 
              key={s.key} 
              className={`p-3.5 bg-white/40 dark:bg-[#0d1117]/40 backdrop-blur-md border border-gray-200/50 dark:border-white/5 hover:border-gray-300/50 dark:hover:border-white/10 transition-colors duration-300 flex flex-col justify-between transition-all rounded-2xl ${
                status === "FAULT"
                  ? "border-red-500/50 bg-red-950/20 text-white shadow-lg shadow-red-500/10"
                  : status === "WARNING"
                  ? "border-amber-500/50 bg-amber-950/20 text-white"
                  : "border-gray-200/50 dark:border-white/10 hover:border-gray-500 text-gray-700 dark:text-gray-200"
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-1.5">
                  <Icon className={`w-4 h-4 ${s.color}`} />
                  <span className="text-[11px] font-bold text-gray-600 dark:text-gray-300 font-mono truncate">{s.name}</span>
                </div>
                {status === "FAULT" && (
                  <span className="px-1.5 py-0.5 bg-red-500/20 text-red-300 text-[9px] font-mono font-bold border border-red-500/40 rounded-2xl">
                    FAULT
                  </span>
                )}
                {status === "WARNING" && (
                  <span className="px-1.5 py-0.5 bg-amber-500/20 text-amber-300 text-[9px] font-mono font-bold border border-amber-500/40 rounded-2xl">
                    DEGRADED
                  </span>
                )}
                {status === "NOMINAL" && (
                  <span className="px-1.5 py-0.5 bg-emerald-500/10 text-emerald-400 text-[9px] font-mono font-bold border border-emerald-500/30 rounded-2xl">
                    OK
                  </span>
                )}
              </div>

              {/* Sensor Live Value & Mini Waveform */}
              <div className="flex items-end justify-between my-1">
                <div>
                  <div className="text-xl font-mono font-black text-white">{displayVal}</div>
                  <div className="text-[10px] text-gray-500 dark:text-gray-400 font-mono">{s.unit}</div>
                </div>

                <div className="opacity-80">
                  {renderSparkline(s.key, sparklineColor)}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

