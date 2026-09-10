import React, { useState } from 'react';
import { Download, Sparkles, X, FileText } from 'lucide-react';
import { downloadSyntheticCsvUrl } from '../api';

export default function SyntheticGeneratorModal({ isOpen, onClose }) {
  const [selectedFault, setSelectedFault] = useState('CYL_3_IGNITION_MISFIRE');

  if (!isOpen) return null;

  const faults = [
    { id: "NO_ISSUE", name: "🟢 Healthy Balanced Engine" },
    { id: "CYL_3_IGNITION_MISFIRE", name: "🔴 Cylinder 3 Ignition Misfire" },
    { id: "CYL_5_INJECTOR_CLOGGING", name: "🟡 Cylinder 5 Injector Restriction" },
    { id: "TURBO_BOOST_LEAK", name: "🔴 Charge Air Boost Pressure Leak" },
    { id: "MAF_SENSOR_DRIFT", name: "🟡 MAF Sensor Calibration Drift" },
    { id: "HEAD_GASKET_BREACH", name: "⚠️ Head Gasket Thermal Breach" },
    { id: "EGR_VALVE_STUCK_OPEN", name: "🟡 EGR Valve Stuck Open" },
    { id: "HPFP_PRESSURE_DROP", name: "🔴 HPFP High Pressure Drop" },
  ];

  const handleDownload = () => {
    const link = document.createElement('a');
    link.href = downloadSyntheticCsvUrl(selectedFault);
    link.download = `ecu_log_${selectedFault.toLowerCase()}_i6.csv`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-[#161b22] border border-[#30363d] rounded-xl max-w-md w-full p-5 shadow-xl relative">
        <button onClick={onClose} className="absolute top-4 right-4 text-gray-400 hover:text-white">
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-2 mb-4">
          <Sparkles className="w-5 h-5 text-cyan-400" />
          <h3 className="text-base font-bold text-white">Generate Custom ECU CSV Test File</h3>
        </div>

        <p className="text-xs text-gray-300 mb-4">
          Synthesize a 30-second high-frequency ECU log with realistic sensor noise and exact fault physics for testing.
        </p>

        <div className="space-y-2 mb-5">
          {faults.map((f) => (
            <label
              key={f.id}
              onClick={() => setSelectedFault(f.id)}
              className={`flex items-center justify-between p-2.5 rounded-lg border text-xs cursor-pointer transition-all ${
                selectedFault === f.id
                  ? 'border-cyan-400 bg-cyan-500/10 text-white'
                  : 'border-[#30363d] bg-[#0d1117] text-gray-300 hover:border-gray-500'
              }`}
            >
              <span>{f.name}</span>
              <input
                type="radio"
                name="fault"
                checked={selectedFault === f.id}
                onChange={() => setSelectedFault(f.id)}
                className="accent-cyan-400"
              />
            </label>
          ))}
        </div>

        <div className="flex justify-end gap-2">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-[#0d1117] border border-[#30363d] hover:bg-[#1c2128] text-gray-300 text-xs font-semibold rounded-lg"
          >
            Cancel
          </button>
          <button
            onClick={handleDownload}
            className="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold rounded-lg flex items-center gap-1.5 shadow"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Download CSV File</span>
          </button>
        </div>
      </div>
    </div>
  );
}
