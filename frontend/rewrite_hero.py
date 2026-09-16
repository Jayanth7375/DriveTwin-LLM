import os

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\components\TelemetryUploader.jsx"

new_content = """import React, { useState, useEffect } from 'react';
import { 
  Upload, 
  FileSpreadsheet, 
  Activity, 
  Link2, 
  Unlink, 
  Settings,
  ShieldCheck,
  LineChart,
  Sparkles,
  CheckCircle2
} from 'lucide-react';
import { 
  fetchEcuComPorts, 
  connectLiveEcu, 
  disconnectLiveEcu,
  fetchLiveTelemetryStream
} from '../api';

export default function TelemetryUploader({ onFileUpload, onLiveStreamUpdate, isLoading }) {
  const [ingestionMode, setIngestionMode] = useState('LIVE_ECU'); // 'LIVE_ECU' or 'FILE_UPLOAD'
  const [dragOver, setDragOver] = useState(false);
  
  // Live ECU State
  const [comPorts, setComPorts] = useState([]);
  const [protocols, setProtocols] = useState([]);
  const [selectedPort, setSelectedPort] = useState('COM3 - USB OBD-II Link (FTDI)');
  const [selectedProtocol, setSelectedProtocol] = useState('SAE J1939 CAN-bus (Heavy Duty Diesel)');
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    try {
      const portsData = await fetchEcuComPorts();
      setComPorts(portsData.ports || []);
      setProtocols(portsData.protocols || []);
    } catch (err) {
      console.error("Failed to load COM ports:", err);
    }
  };

  const handleConnectLiveEcu = async () => {
    try {
      const res = await connectLiveEcu({
        port: selectedPort,
        baud_rate: 115200,
        protocol: selectedProtocol
      });
      setIsConnected(true);
      
      const streamRes = await fetchLiveTelemetryStream();
      onLiveStreamUpdate(streamRes);
    } catch (err) {
      console.error("Failed to connect ECU:", err);
      alert("Failed to connect to ECU hardware.");
    }
  };

  const handleDisconnectLiveEcu = async () => {
    try {
      await disconnectLiveEcu();
      setIsConnected(false);
    } catch (err) {
      console.error("Failed to disconnect ECU:", err);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      onFileUpload(e.target.files[0]);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onFileUpload(e.dataTransfer.files[0]);
    }
  };

  return (
    <div className="flex flex-col xl:flex-row items-center justify-between gap-10 w-full mb-8">
      
      {/* LEFT: HERO TEXT */}
      <div className="flex-1 space-y-6">
        <div className="flex items-center gap-4">
          <div className="h-0.5 w-10 bg-cyan-500 rounded-full"></div>
          <span className="text-xs font-mono font-semibold tracking-widest text-gray-500 dark:text-gray-400 uppercase">
            Real-Time Engine Intelligence
          </span>
        </div>
        
        <h1 className="text-5xl lg:text-6xl font-black text-gray-900 dark:text-white leading-[1.1] tracking-tight">
          Keep Your Engine <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-500">
            One Step Ahead
          </span>
        </h1>
        
        <p className="text-gray-600 dark:text-gray-400 max-w-lg text-lg">
          Connect, monitor and analyze your engine with AI-powered diagnostics.
        </p>
        
        {/* Badges */}
        <div className="flex flex-wrap gap-6 pt-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-full bg-emerald-500/10 flex items-center justify-center border border-emerald-500/20 shadow-[0_0_15px_rgba(16,185,129,0.15)]">
              <ShieldCheck className="w-6 h-6 text-emerald-500" />
            </div>
            <div>
              <p className="text-sm font-bold text-gray-900 dark:text-white">Detect</p>
              <p className="text-xs text-gray-500 dark:text-gray-400">Faults Early</p>
            </div>
          </div>
          
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-full bg-blue-500/10 flex items-center justify-center border border-blue-500/20 shadow-[0_0_15px_rgba(59,130,246,0.15)]">
              <LineChart className="w-6 h-6 text-blue-500" />
            </div>
            <div>
              <p className="text-sm font-bold text-gray-900 dark:text-white">Monitor</p>
              <p className="text-xs text-gray-500 dark:text-gray-400">In Real-Time</p>
            </div>
          </div>
          
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-full bg-cyan-500/10 flex items-center justify-center border border-cyan-500/20 shadow-[0_0_15px_rgba(34,211,238,0.15)]">
              <Sparkles className="w-6 h-6 text-cyan-400" />
            </div>
            <div>
              <p className="text-sm font-bold text-gray-900 dark:text-white">Predict</p>
              <p className="text-xs text-gray-500 dark:text-gray-400">With AI</p>
            </div>
          </div>
        </div>
      </div>

      {/* CENTER: 3D ENGINE */}
      <div className="flex-1 flex justify-center relative hidden lg:flex pointer-events-none">
        <div className="absolute inset-0 bg-gradient-to-t from-[#090c10] via-transparent to-transparent z-10 rounded-3xl mix-blend-multiply"></div>
        <img 
          src="/engine-render.jpg" 
          alt="3D Engine Render" 
          className="max-w-[120%] lg:max-w-[140%] object-contain scale-110 drop-shadow-[0_0_50px_rgba(34,211,238,0.15)]"
          style={{ mixBlendMode: 'screen' }}
        />
      </div>

      {/* RIGHT: ECU CONNECTION CARD */}
      <div className="flex-1 w-full max-w-md">
        <div className="bg-white/10 dark:bg-[#161b22]/40 backdrop-blur-2xl border border-gray-200/50 dark:border-white/10 rounded-3xl p-6 shadow-2xl relative overflow-hidden">
          
          {/* Subtle Glows */}
          <div className="absolute -top-10 -right-10 w-40 h-40 bg-emerald-500/20 rounded-full blur-[50px] pointer-events-none"></div>
          
          {/* Mode Switcher */}
          <div className="flex bg-gray-100 dark:bg-[#0d1117]/80 rounded-2xl p-1 mb-6 border border-gray-200/50 dark:border-white/5">
            <button
              onClick={() => setIngestionMode('LIVE_ECU')}
              className={`flex-1 py-2 text-xs font-bold rounded-xl transition-all duration-300 ${ingestionMode === 'LIVE_ECU' ? 'bg-white dark:bg-[#161b22] text-gray-900 dark:text-white shadow-sm border border-gray-200/50 dark:border-white/10' : 'text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'}`}
            >
              Hardware ECU
            </button>
            <button
              onClick={() => setIngestionMode('FILE_UPLOAD')}
              className={`flex-1 py-2 text-xs font-bold rounded-xl transition-all duration-300 ${ingestionMode === 'FILE_UPLOAD' ? 'bg-white dark:bg-[#161b22] text-gray-900 dark:text-white shadow-sm border border-gray-200/50 dark:border-white/10' : 'text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'}`}
            >
              Dataset CSV
            </button>
          </div>
          
          {ingestionMode === 'LIVE_ECU' ? (
            <div className="space-y-5 relative z-10">
              <div className="flex items-start gap-4 mb-2">
                <div className="w-10 h-10 rounded-2xl bg-emerald-500/10 flex items-center justify-center shrink-0 border border-emerald-500/20">
                  <Link2 className="w-5 h-5 text-emerald-400" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-gray-900 dark:text-white">Connect to ECU</h3>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Select your hardware and vehicle protocol.</p>
                </div>
              </div>

              <div className="space-y-4 pt-2">
                <div>
                  <label className="text-[11px] font-semibold text-gray-500 dark:text-gray-400 block mb-1.5 uppercase tracking-wider">COM Port / Adapter</label>
                  <div className="relative">
                    <Settings className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
                    <select
                      value={selectedPort}
                      onChange={(e) => setSelectedPort(e.target.value)}
                      disabled={isConnected}
                      className="w-full bg-gray-50 dark:bg-[#0d1117]/80 border border-gray-200 dark:border-white/10 rounded-xl pl-9 pr-4 py-2.5 text-sm text-gray-900 dark:text-white focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500 transition-all appearance-none outline-none"
                    >
                      <option>COM3 - USB OBD-II Link (FTDI)</option>
                      <option>COM4 - Vector CANcaseXL</option>
                      <option>Bluetooth OBDLink MX+</option>
                      {comPorts.map(p => <option key={p}>{p}</option>)}
                    </select>
                  </div>
                </div>

                <div>
                  <label className="text-[11px] font-semibold text-gray-500 dark:text-gray-400 block mb-1.5 uppercase tracking-wider">Vehicle Protocol</label>
                  <div className="relative">
                    <Activity className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
                    <select
                      value={selectedProtocol}
                      onChange={(e) => setSelectedProtocol(e.target.value)}
                      disabled={isConnected}
                      className="w-full bg-gray-50 dark:bg-[#0d1117]/80 border border-gray-200 dark:border-white/10 rounded-xl pl-9 pr-4 py-2.5 text-sm text-gray-900 dark:text-white focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500 transition-all appearance-none outline-none"
                    >
                      <option>SAE J1939 CAN-bus (Heavy Duty Diesel)</option>
                      <option>ISO 15765-4 CAN (11 bit ID, 500 Kbaud)</option>
                      {protocols.map(p => <option key={p}>{p}</option>)}
                    </select>
                  </div>
                </div>

                <div className="pt-2">
                  {!isConnected ? (
                    <button
                      onClick={handleConnectLiveEcu}
                      className="w-full py-3 bg-gradient-to-r from-emerald-500 to-emerald-600 hover:from-emerald-400 hover:to-emerald-500 text-white text-sm font-bold rounded-xl flex items-center justify-center gap-2 transition-all shadow-[0_0_20px_rgba(16,185,129,0.3)] hover:shadow-[0_0_25px_rgba(16,185,129,0.5)] hover:-translate-y-0.5"
                    >
                      <CheckCircle2 className="w-4 h-4" />
                      Connect to ECU
                    </button>
                  ) : (
                    <button
                      onClick={handleDisconnectLiveEcu}
                      className="w-full py-3 bg-red-500/10 hover:bg-red-500/20 text-red-500 border border-red-500/20 text-sm font-bold rounded-xl flex items-center justify-center gap-2 transition-all"
                    >
                      <Unlink className="w-4 h-4" />
                      Disconnect
                    </button>
                  )}
                </div>
                
                <p className="text-[10px] text-gray-400 dark:text-gray-500 text-center mt-4">
                  Connect via USB FTDI, Bluetooth OBDLink MX+, or Vector CANcaseXL.
                </p>
              </div>
            </div>
          ) : (
            <div className="space-y-4 relative z-10">
               <div className="flex items-start gap-4 mb-4">
                <div className="w-10 h-10 rounded-2xl bg-cyan-500/10 flex items-center justify-center shrink-0 border border-cyan-500/20">
                  <FileSpreadsheet className="w-5 h-5 text-cyan-400" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-gray-900 dark:text-white">Upload Telemetry</h3>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Analyze a massive ECU data dump instantly.</p>
                </div>
              </div>
              
              <div 
                className={`border-2 border-dashed rounded-2xl p-8 text-center transition-all duration-300 ${
                  dragOver ? 'border-cyan-400 bg-cyan-500/5' : 'border-gray-300 dark:border-white/10 hover:border-cyan-500/50 bg-gray-50 dark:bg-[#0d1117]/50'
                }`}
                onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
                onDragLeave={() => setDragOver(false)}
                onDrop={handleDrop}
              >
                <Upload className={`w-10 h-10 mx-auto mb-4 transition-colors ${dragOver ? 'text-cyan-400' : 'text-gray-400 dark:text-gray-500'}`} />
                <p className="text-sm font-semibold text-gray-900 dark:text-white">
                  Drag & drop CSV or Excel here
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-2 mb-6">
                  Supports standard ECU log formats
                </p>
                
                <label className="inline-flex items-center gap-2 px-6 py-2.5 bg-gray-100 hover:bg-gray-200 dark:bg-white/10 dark:hover:bg-white/20 text-gray-900 dark:text-white text-sm font-bold rounded-xl cursor-pointer transition-all">
                  <span>Browse File</span>
                  <input type="file" className="hidden" accept=".csv,.xlsx,.xls" onChange={handleFileChange} />
                </label>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
"""

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)

