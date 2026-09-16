import React from 'react';
import { 
  AlertTriangle, 
  CheckCircle, 
  Crosshair,
  Cpu,
  Target,
  Gauge
} from 'lucide-react';

const CircularProgress = ({ percentage, colorClass, size = 100, strokeWidth = 8, label }) => {
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const offset = circumference - (percentage / 100) * circumference;
  
  return (
    <div className="relative flex items-center justify-center" style={{ width: size, height: size }}>
      <svg className="transform -rotate-90 w-full h-full">
        <circle 
          cx={size / 2} cy={size / 2} r={radius} 
          className="stroke-gray-200 dark:stroke-white/5" 
          strokeWidth={strokeWidth} 
          fill="none" 
        />
        <circle 
          cx={size / 2} cy={size / 2} r={radius} 
          className={colorClass} 
          strokeWidth={strokeWidth} 
          strokeDasharray={circumference} 
          strokeDashoffset={offset} 
          strokeLinecap="round" 
          fill="none" 
          style={{ transition: 'stroke-dashoffset 1s ease-out' }}
        />
      </svg>
      <div className="absolute flex flex-col items-center justify-center text-center">
        <span className="text-xl font-black text-gray-900 dark:text-white">{percentage.toFixed(1)}%</span>
        {label && <span className="text-[9px] uppercase tracking-wider text-gray-500 font-bold">{label}</span>}
      </div>
    </div>
  );
};

export default function DiagnosticCard({ report }) {
  if (!report) return null;

  const severity = report.ml_prediction?.severity || 'LOW';
  const confidence = report.ml_prediction?.confidence_score * 100 || 0;
  const pinnProb = report.ml_prediction?.pinn_transformer?.probability * 100 || 0;
  
  const hasIssue = severity === 'HIGH' || severity === 'CRITICAL';
  
  const getSeverityColor = (sev) => {
    switch (sev) {
      case 'CRITICAL': return 'border-red-500/50 bg-red-500/10 text-red-500 shadow-[0_0_15px_rgba(239,68,68,0.2)]';
      case 'HIGH': return 'border-orange-500/50 bg-orange-500/10 text-orange-500 shadow-[0_0_15px_rgba(249,115,22,0.2)]';
      case 'MEDIUM': return 'border-yellow-500/50 bg-yellow-500/10 text-yellow-500 shadow-[0_0_15px_rgba(234,179,8,0.2)]';
      default: return 'border-emerald-500/50 bg-emerald-500/10 text-emerald-500 shadow-[0_0_15px_rgba(16,185,129,0.2)]';
    }
  };

  return (
    <div className="bg-white/60 dark:bg-[#161b22]/60 backdrop-blur-xl border border-gray-200/50 dark:border-white/10 rounded-3xl p-6 shadow-2xl transition-all duration-300">
      
      {/* HEADER */}
      <div className="flex items-center justify-between mb-6 pb-4 border-b border-gray-200/50 dark:border-white/10">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-xl bg-blue-500/10 flex items-center justify-center border border-blue-500/20">
            <Crosshair className="w-4 h-4 text-blue-500" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-gray-900 dark:text-white leading-none mb-1">Diagnostic Overview</h2>
            <p className="text-xs text-gray-500 dark:text-gray-400">AI analysis of live engine data</p>
          </div>
        </div>
        
        <div className="flex items-center gap-3">
          <span className="text-[11px] font-mono font-bold bg-emerald-500/10 text-emerald-400 px-3 py-1.5 border border-emerald-500/20 rounded-full flex items-center gap-2">
            <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></div>
            OBD-II / J1939 Active
          </span>
        </div>
      </div>

      {/* GRID */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
        
        {/* Box 1: Status */}
        <div className={`p-5 rounded-2xl border flex flex-col justify-center transition-all ${
          hasIssue 
            ? 'bg-red-500/5 border-red-500/30 shadow-[inset_0_0_20px_rgba(239,68,68,0.05)]' 
            : 'bg-emerald-500/5 border-emerald-500/30'
        }`}>
          <div className="flex items-start gap-4">
            <div className={`w-10 h-10 rounded-full flex items-center justify-center shrink-0 ${hasIssue ? 'bg-red-500/20 text-red-500' : 'bg-emerald-500/20 text-emerald-500'}`}>
              {hasIssue ? <AlertTriangle className="w-5 h-5" /> : <CheckCircle className="w-5 h-5" />}
            </div>
            <div>
              <p className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-1">System Issue Status</p>
              <h3 className={`text-lg font-black tracking-tight ${hasIssue ? 'text-red-500' : 'text-emerald-500'}`}>
                {hasIssue ? 'ISSUE DETECTED' : 'SYSTEM OPTIMAL'}
              </h3>
              <p className="text-xs font-mono font-bold text-gray-900 dark:text-white mt-1">
                {report.ml_prediction?.top_prediction || 'NO_FAULTS_DETECTED'}
              </p>
            </div>
          </div>
          <div className="mt-4 pt-4 border-t border-gray-200/50 dark:border-white/5">
            <p className="text-xs text-gray-500 dark:text-gray-400">
              Subsystem: <span className="font-semibold text-gray-900 dark:text-gray-200">{report.ml_prediction?.subsystem || 'N/A'}</span>
            </p>
          </div>
        </div>

        {/* Box 2: Location */}
        <div className="p-5 rounded-2xl bg-blue-500/5 border border-blue-500/20 shadow-[inset_0_0_20px_rgba(59,130,246,0.05)] flex flex-col justify-center transition-all">
          <div className="flex items-start gap-4">
            <div className="w-10 h-10 rounded-full bg-blue-500/20 text-blue-500 flex items-center justify-center shrink-0">
              <Cpu className="w-5 h-5" />
            </div>
            <div>
              <p className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-1">Isolated Problem Location</p>
              <h3 className="text-lg font-black text-cyan-500 dark:text-cyan-400 tracking-tight leading-tight">
                {report.ml_prediction?.isolated_component || 'Engine Block'}
              </h3>
            </div>
          </div>
          <div className="mt-4 pt-4 border-t border-gray-200/50 dark:border-white/5">
            <p className="text-xs text-gray-500 dark:text-gray-400">
              Targeted for OEM Repair Workflow
            </p>
          </div>
        </div>

        {/* Box 3: Confidence */}
        <div className="p-5 rounded-2xl bg-emerald-500/5 border border-emerald-500/20 flex flex-col justify-between transition-all relative overflow-hidden">
          <div className="absolute top-4 left-4 w-8 h-8 rounded-full bg-emerald-500/20 flex items-center justify-center">
            <Target className="w-4 h-4 text-emerald-500" />
          </div>
          <div className="text-right">
             <p className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Overall Confidence Score</p>
          </div>
          
          <div className="flex items-center justify-between mt-4">
             <CircularProgress 
               percentage={confidence} 
               colorClass="stroke-emerald-400" 
               label="Ensemble"
             />
             <div className="text-right">
                <p className="text-xs font-bold text-emerald-500 dark:text-emerald-400">Ensemble</p>
                <p className="text-[10px] text-gray-500 mt-1 max-w-[100px] leading-tight">Physics + ML Multi-Model Agreement</p>
             </div>
          </div>
        </div>

        {/* Box 4: PINN */}
        <div className="p-5 rounded-2xl bg-purple-500/5 border border-purple-500/20 flex flex-col justify-between transition-all relative overflow-hidden">
          <div className="absolute top-4 left-4 w-8 h-8 rounded-full bg-purple-500/20 flex items-center justify-center">
            <Gauge className="w-4 h-4 text-purple-500" />
          </div>
          <div className="text-right">
             <p className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Custom PyTorch PINN Score</p>
          </div>
          
          <div className="flex items-center justify-between mt-4">
             <CircularProgress 
               percentage={pinnProb} 
               colorClass="stroke-purple-400" 
               label="CPU"
             />
             <div className="text-right flex flex-col items-end">
                <p className="text-xs font-bold text-purple-500 dark:text-purple-400 mb-1">CPU</p>
                <p className="text-[9px] text-gray-500 max-w-[90px] truncate" title={report.ml_prediction?.pinn_transformer?.predicted_class}>
                  Top: {report.ml_prediction?.pinn_transformer?.predicted_class || 'N/A'}
                </p>
             </div>
          </div>
        </div>

      </div>
    </div>
  );
}
