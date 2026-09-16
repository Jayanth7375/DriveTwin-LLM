import os

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\components\LiveTelemetrySheet.jsx"

new_content = """import React, { useState, useEffect } from 'react';
import { 
  Activity, 
  Settings, 
  Wind, 
  Gauge,
  Thermometer,
  Zap,
  Play,
  Pause,
  Clock,
  LineChart,
  RefreshCw,
  BarChart2
} from 'lucide-react';

export default function LiveTelemetrySheet({ telemetryPreview, latestSensors, physicsSummary, mlPrediction }) {
  const [history, setHistory] = useState([]);
  const [playbackIndex, setPlaybackIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(true);
  const [speedMs, setSpeedMs] = useState(80); 

  useEffect(() => {
    if (telemetryPreview && telemetryPreview.length > 0) {
      setPlaybackIndex(0);
      setIsPlaying(true);
      setHistory([telemetryPreview[0]]);
    }
  }, [telemetryPreview]);

  useEffect(() => {
    let timer = null;
    if (isPlaying && telemetryPreview && telemetryPreview.length > 0) {
      timer = setInterval(() => {
        setPlaybackIndex((prev) => {
          const next = prev + 1;
          if (next >= telemetryPreview.length) {
            setIsPlaying(false);
            return prev;
          }
          setHistory(h => {
            const newHistory = [...h, telemetryPreview[next]];
            if (newHistory.length > 30) newHistory.shift();
            return newHistory;
          });
          return next;
        });
      }, speedMs);
    }
    return () => {
      if (timer) clearInterval(timer);
    };
  }, [isPlaying, telemetryPreview, speedMs]);

  const currentSensors = (telemetryPreview && telemetryPreview.length > 0)
    ? telemetryPreview[playbackIndex]
    : latestSensors;

  const totalRows = telemetryPreview ? telemetryPreview.length : 1;
  const currentTime = currentSensors?.Time_s !== undefined 
    ? `${currentSensors.Time_s.toFixed(1)}s`
    : `${(playbackIndex * 0.1).toFixed(1)}s`;
  const totalTime = (telemetryPreview && telemetryPreview.length > 0 && telemetryPreview[telemetryPreview.length - 1]?.Time_s)
    ? `${telemetryPreview[telemetryPreview.length - 1].Time_s.toFixed(1)}s`
    : `${(totalRows * 0.1).toFixed(1)}s`;

  // Mini Chart renderer
  const renderSparkline = (dataKey, strokeColor = "#10b981") => {
    if (!history || history.length < 2) return <div className="h-10"></div>;
    const values = history.map(h => h[dataKey] || 0);
    const min = Math.min(...values);
    const max = Math.max(...values);
    const range = (max - min) || 1;
    
    const width = 100;
    const height = 30;
    
    const points = values.map((val, i) => {
      const x = (i / (values.length - 1)) * width;
      const y = height - ((val - min) / range) * height;
      return `${x},${y}`;
    }).join(" ");
    
    return (
      <svg width="100%" height="40" viewBox={`0 0 ${width} ${height}`} className="overflow-visible mt-2">
        <polyline
          fill="none"
          stroke={strokeColor}
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          points={points}
        />
        {/* Glow effect */}
        <polyline
          fill="none"
          stroke={strokeColor}
          strokeWidth="6"
          strokeLinecap="round"
          strokeLinejoin="round"
          points={points}
          opacity="0.2"
          filter="blur(2px)"
        />
      </svg>
    );
  };
  
  // Large dynamic chart renderer
  const renderDynamicChart = (dataKey, strokeColor = "#10b981") => {
    if (!history || history.length < 2) return <div className="h-24"></div>;
    const values = history.map(h => h[dataKey] || 0);
    const min = Math.min(...values);
    const max = Math.max(...values);
    const range = (max - min) || 1;
    
    const width = 800;
    const height = 80;
    
    const points = values.map((val, i) => {
      const x = (i / (values.length - 1)) * width;
      const y = height - ((val - min) / range) * height;
      return `${x},${y}`;
    }).join(" ");
    
    const fillPoints = `0,${height} ${points} ${width},${height}`;
    
    return (
      <svg width="100%" height="100" viewBox={`0 0 ${width} ${height}`} className="overflow-visible preserve-3d">
        <defs>
          <linearGradient id={`gradient-${dataKey}`} x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={strokeColor} stopOpacity="0.3" />
            <stop offset="100%" stopColor={strokeColor} stopOpacity="0.0" />
          </linearGradient>
        </defs>
        <polygon
          points={fillPoints}
          fill={`url(#gradient-${dataKey})`}
        />
        <polyline
          fill="none"
          stroke={strokeColor}
          strokeWidth="3"
          strokeLinecap="round"
          strokeLinejoin="round"
          points={points}
        />
      </svg>
    );
  };

  return (
    <div className="bg-white/60 dark:bg-[#161b22]/60 backdrop-blur-xl border border-gray-200/50 dark:border-white/10 rounded-3xl p-6 shadow-2xl transition-all duration-300 flex flex-col gap-6">
      
      {/* HEADER */}
      <div className="flex flex-col md:flex-row md:items-center justify-between border-b border-gray-200/50 dark:border-white/10 pb-4 gap-4">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-xl bg-blue-500/10 flex items-center justify-center border border-blue-500/20">
            <BarChart2 className="w-4 h-4 text-blue-500" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-gray-900 dark:text-white leading-none mb-1">
              Live Telemetry
            </h3>
            <span className="text-xs text-gray-500 dark:text-gray-400">
              Dynamic row-by-row playback from telemetry log.
            </span>
          </div>
        </div>

        {/* Playback Controls */}
        <div className="flex items-center gap-3 text-xs font-mono">
          <button
            onClick={() => setIsPlaying(!isPlaying)}
            className="px-4 py-2 bg-emerald-500 hover:bg-emerald-400 text-white font-bold flex items-center gap-2 rounded-xl shadow-[0_0_15px_rgba(16,185,129,0.3)] transition-all"
          >
            {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
            <span>{isPlaying ? 'Pause Live' : 'Play Live'}</span>
          </button>
          
          <button 
            onClick={() => { setPlaybackIndex(0); setHistory(telemetryPreview ? [telemetryPreview[0]] : []); }}
            className="w-8 h-8 flex items-center justify-center bg-gray-100 dark:bg-white/5 hover:bg-gray-200 dark:hover:bg-white/10 text-gray-600 dark:text-gray-300 rounded-lg transition-colors border border-gray-200/50 dark:border-white/10"
          >
            <RefreshCw className="w-4 h-4" />
          </button>

          <div className="flex items-center gap-2 px-3 py-1.5 bg-gray-100 dark:bg-white/5 border border-gray-200/50 dark:border-white/10 rounded-lg text-gray-600 dark:text-gray-300">
            <Clock className="w-3.5 h-3.5 text-cyan-500" />
            <span>{currentTime} / {totalTime}</span>
          </div>
          
          <select 
            value={speedMs} 
            onChange={(e) => setSpeedMs(Number(e.target.value))}
            className="bg-gray-100 dark:bg-white/5 border border-gray-200/50 dark:border-white/10 text-gray-600 dark:text-gray-300 rounded-lg px-2 py-1.5 outline-none"
          >
            <option value={160}>0.5x Slower</option>
            <option value={80}>1x Normal</option>
            <option value={20}>4x Fast</option>
          </select>
        </div>
      </div>

      {/* METRICS ROW */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        
        {/* RPM */}
        <div className="p-4 rounded-2xl bg-gray-50/50 dark:bg-[#0d1117]/50 border border-gray-200/50 dark:border-white/5">
          <p className="text-xs font-semibold text-gray-500 dark:text-gray-400 mb-1">Engine Speed</p>
          <div className="flex items-baseline gap-1">
            <h3 className="text-2xl font-black text-gray-900 dark:text-white">{(currentSensors?.RPM || 0).toFixed(0)}</h3>
            <span className="text-xs text-gray-500">RPM</span>
          </div>
          {renderSparkline("RPM", "#10b981")}
        </div>

        {/* Coolant */}
        <div className="p-4 rounded-2xl bg-gray-50/50 dark:bg-[#0d1117]/50 border border-gray-200/50 dark:border-white/5">
          <p className="text-xs font-semibold text-gray-500 dark:text-gray-400 mb-1">Coolant Temp</p>
          <div className="flex items-baseline gap-1">
            <h3 className="text-2xl font-black text-gray-900 dark:text-white">{(currentSensors?.Coolant_Temp || 0).toFixed(1)}</h3>
            <span className="text-xs text-gray-500">°C</span>
          </div>
          {renderSparkline("Coolant_Temp", "#ef4444")}
        </div>

        {/* Boost Pressure */}
        <div className="p-4 rounded-2xl bg-gray-50/50 dark:bg-[#0d1117]/50 border border-gray-200/50 dark:border-white/5">
          <p className="text-xs font-semibold text-gray-500 dark:text-gray-400 mb-1">Boost Pressure</p>
          <div className="flex items-baseline gap-1">
            <h3 className="text-2xl font-black text-gray-900 dark:text-white">{(currentSensors?.Boost_Pressure || 0).toFixed(1)}</h3>
            <span className="text-xs text-gray-500">kPa</span>
          </div>
          {renderSparkline("Boost_Pressure", "#f59e0b")}
        </div>

        {/* MAF */}
        <div className="p-4 rounded-2xl bg-gray-50/50 dark:bg-[#0d1117]/50 border border-gray-200/50 dark:border-white/5">
          <p className="text-xs font-semibold text-gray-500 dark:text-gray-400 mb-1">Mass Air Flow</p>
          <div className="flex items-baseline gap-1">
            <h3 className="text-2xl font-black text-gray-900 dark:text-white">{(currentSensors?.MAF || 0).toFixed(1)}</h3>
            <span className="text-xs text-gray-500">g/s</span>
          </div>
          {renderSparkline("MAF", "#3b82f6")}
        </div>
        
      </div>

      {/* WIDE OSCILLOSCOPE */}
      <div className="p-5 rounded-2xl bg-gray-50/50 dark:bg-[#0d1117]/50 border border-gray-200/50 dark:border-white/5">
        <div className="flex items-center justify-between mb-4">
          <p className="text-xs font-bold text-gray-900 dark:text-white">Sensor Signal (Dynamic)</p>
          <div className="flex items-center gap-2">
            <span className="text-[10px] text-gray-500">Engine Speed (RPM)</span>
            <div className="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_5px_#10b981]"></div>
          </div>
        </div>
        {renderDynamicChart("RPM", "#10b981")}
        <div className="flex justify-between mt-2 px-2 text-[10px] text-gray-500 font-mono">
          <span>{history.length > 0 ? (history[0].Time_s || 0).toFixed(1) : 0}s</span>
          <span>{currentTime}</span>
        </div>
      </div>
      
    </div>
  );
}
"""

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)

