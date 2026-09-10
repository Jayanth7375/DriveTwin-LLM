import React, { useState, useEffect } from 'react';
import { 
  Upload, 
  FileSpreadsheet, 
  Radio, 
  Zap, 
  Unplug, 
  Activity
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
      console.error("Initialization fetch error:", err);
    }
  };

  const handleConnectLiveEcu = async () => {
    try {
      const res = await connectLiveEcu({
        port: selectedPort,
        baud_rate: 115200,
        protocol: selectedProtocol,
        fault_injection: "CYL_3_IGNITION_MISFIRE"
      });
      setIsConnected(true);
      
      const streamRes = await fetchLiveTelemetryStream();
      onLiveStreamUpdate(streamRes);
    } catch (err) {
      alert("Failed to connect to ECU interface: " + err.message);
    }
  };

  const handleDisconnectLiveEcu = async () => {
    try {
      await disconnectLiveEcu();
      setIsConnected(false);
    } catch (err) {
      console.error("Disconnect error:", err);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      onFileUpload(e.target.files[0]);
    }
  };

  return (
    <div className="bg-[#161b22] border border-[#30363d] rounded-none p-5 shadow-sm space-y-5">
      {/* Primary Ingestion Mode Switcher */}
      <div className="flex items-center justify-between border-b border-[#30363d] pb-3">
        <div className="flex items-center gap-2">
          <button
            onClick={() => setIngestionMode('LIVE_ECU')}
            className={`flex items-center gap-2 px-4 py-2 rounded-none text-xs font-bold transition-all ${
              ingestionMode === 'LIVE_ECU'
                ? 'bg-cyan-600 text-white shadow border border-cyan-400'
                : 'bg-[#0d1117] text-gray-400 hover:text-white border border-[#30363d]'
            }`}
          >
            <Radio className={`w-4 h-4 ${ingestionMode === 'LIVE_ECU' ? 'animate-pulse text-white' : 'text-cyan-400'}`} />
            <span>Connect Live ECU Data</span>
          </button>

          <button
            onClick={() => setIngestionMode('FILE_UPLOAD')}
            className={`flex items-center gap-2 px-4 py-2 rounded-none text-xs font-bold transition-all ${
              ingestionMode === 'FILE_UPLOAD'
                ? 'bg-cyan-600 text-white shadow border border-cyan-400'
                : 'bg-[#0d1117] text-gray-400 hover:text-white border border-[#30363d]'
            }`}
          >
            <FileSpreadsheet className={`w-4 h-4 ${ingestionMode === 'FILE_UPLOAD' ? 'text-white' : 'text-cyan-400'}`} />
            <span>Upload Data from CSV / Excel</span>
          </button>
        </div>

        <span className="text-[11px] font-mono text-cyan-400 bg-cyan-500/10 px-2.5 py-1 border border-cyan-500/30 hidden md:inline-block rounded-none">
          {ingestionMode === 'LIVE_ECU' ? 'OBD-II / J1939 Active' : 'CSV / XLSX Support'}
        </span>
      </div>

      {/* MODE 1: CONNECT LIVE ECU UNIT */}
      {ingestionMode === 'LIVE_ECU' && (
        <div className="bg-[#0d1117] border border-[#30363d] rounded-none p-5 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <Zap className="w-4 h-4 text-emerald-400" />
                Physical ECU Hardware & Adapter Connection
              </h3>
              <p className="text-xs text-gray-400 mt-0.5">
                Connect via USB FTDI, Bluetooth OBDLink MX+, or Vector CANcaseXL (SAE J1939 Diesel Protocol).
              </p>
            </div>

            <div className="flex items-center gap-2">
              {isConnected ? (
                <span className="text-xs font-mono text-emerald-400 bg-emerald-500/10 px-3 py-1.5 border border-emerald-500/30 flex items-center gap-1.5 animate-pulse rounded-none">
                  <Activity className="w-3.5 h-3.5" />
                  <span>CONNECTED & STREAMING (100 Hz)</span>
                </span>
              ) : (
                <span className="text-xs font-mono text-gray-400 bg-[#161b22] px-3 py-1.5 border border-[#30363d] rounded-none">
                  DISCONNECTED
                </span>
              )}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
            <div>
              <label className="text-xs font-semibold text-gray-300 block mb-1.5">
                Select COM Port / Adapter:
              </label>
              <select
                value={selectedPort}
                onChange={(e) => setSelectedPort(e.target.value)}
                disabled={isConnected}
                className="w-full bg-[#161b22] border border-[#30363d] rounded-none px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-400"
              >
                {comPorts.map((p, idx) => (
                  <option key={idx} value={p}>{p}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="text-xs font-semibold text-gray-300 block mb-1.5">
                Select Vehicle Protocol:
              </label>
              <select
                value={selectedProtocol}
                onChange={(e) => setSelectedProtocol(e.target.value)}
                disabled={isConnected}
                className="w-full bg-[#161b22] border border-[#30363d] rounded-none px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-400"
              >
                {protocols.map((pr, idx) => (
                  <option key={idx} value={pr}>{pr}</option>
                ))}
              </select>
            </div>

            <div className="flex items-end">
              {!isConnected ? (
                <button
                  onClick={handleConnectLiveEcu}
                  className="w-full py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold rounded-none flex items-center justify-center gap-2 transition-colors shadow"
                >
                  <Zap className="w-4 h-4" />
                  <span>Connect Live ECU Hardware</span>
                </button>
              ) : (
                <button
                  onClick={handleDisconnectLiveEcu}
                  className="w-full py-2 bg-red-600/30 hover:bg-red-600/40 text-red-300 border border-red-500/40 text-xs font-bold rounded-none flex items-center justify-center gap-2 transition-colors"
                >
                  <Unplug className="w-4 h-4" />
                  <span>Disconnect Live Stream</span>
                </button>
              )}
            </div>
          </div>
        </div>
      )}

      {/* MODE 2: SINGLE CLEAN UPLOAD OPTION FOR CSV / EXCEL */}
      {ingestionMode === 'FILE_UPLOAD' && (
        <div
          onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={() => setDragOver(false)}
          onDrop={(e) => {
            e.preventDefault();
            setDragOver(false);
            if (e.dataTransfer.files && e.dataTransfer.files[0]) {
              onFileUpload(e.dataTransfer.files[0]);
            }
          }}
          className={`border-2 border-dashed rounded-none p-8 text-center transition-all flex flex-col items-center justify-center ${
            dragOver
              ? 'border-cyan-400 bg-cyan-500/10'
              : 'border-[#30363d] hover:border-gray-500 bg-[#0d1117]'
          }`}
        >
          <Upload className="w-9 h-9 text-cyan-400 mb-3 animate-bounce" />
          <p className="text-sm font-semibold text-white">
            Drag & drop ECU telemetry CSV or Excel file here
          </p>
          <p className="text-xs text-gray-400 mt-1 mb-4">
            Supports standard ECU log formats (.csv, .xlsx, .xls)
          </p>
          <label className="inline-flex items-center gap-2 px-5 py-2 bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-bold rounded-none cursor-pointer transition-colors shadow-lg">
            <span>Browse Telemetry File</span>
            <input type="file" accept=".csv,.xlsx,.xls" onChange={handleFileChange} className="hidden" />
          </label>
        </div>
      )}
    </div>
  );
}
