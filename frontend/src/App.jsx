import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import TelemetryUploader from './components/TelemetryUploader';
import EngineSchematicI6 from './components/EngineSchematicI6';
import DiagnosticCard from './components/DiagnosticCard';
import PhysicsTelemetryCharts from './components/PhysicsTelemetryCharts';
import LLMReportView from './components/LLMReportView';
import InteractiveChat from './components/InteractiveChat';
import SyntheticGeneratorModal from './components/SyntheticGeneratorModal';
import DatasetManagerPage from './components/DatasetManagerPage';
import DigitalTwinView from './components/DigitalTwinView';
import LiveTelemetrySheet from './components/LiveTelemetrySheet';
import { uploadEcuFile, analyzeSampleScenario, analyzeDatasetFile } from './api';
import { 
  FileSpreadsheet, 
  Activity, 
  BarChart3, 
  Sparkles, 
  MessageSquare, 
  Database, 
  RefreshCw,
  Gauge,
  Cpu
} from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('overview'); // 'overview', 'llm', 'digitaltwin', 'schematic', 'physics', 'chat', 'dataset'
  const [analysisData, setAnalysisData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeScenario, setActiveScenario] = useState('CYL_3_IGNITION_MISFIRE');
  const [isGeneratorOpen, setIsGeneratorOpen] = useState(false);
  const [hardwareInfo, setHardwareInfo] = useState('');

  // Initial load with default scenario
  useEffect(() => {
    handleSampleSelect('CYL_3_IGNITION_MISFIRE');
  }, []);

  const handleLiveStreamUpdate = (data) => {
    setAnalysisData(data);
    if (data.diagnostic_report?.hardware_device) {
      setHardwareInfo(data.diagnostic_report.hardware_device);
    }
  };

  const handleFileUpload = async (file) => {
    setLoading(true);
    setActiveScenario(null);
    try {
      const data = await uploadEcuFile(file);
      setAnalysisData(data);
      if (data.diagnostic_report?.hardware_device) {
        setHardwareInfo(data.diagnostic_report.hardware_device);
      }
    } catch (err) {
      alert("Error analyzing ECU file: " + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleDatasetFileSelect = async (relativePath) => {
    setLoading(true);
    setActiveScenario(null);
    try {
      const data = await analyzeDatasetFile(relativePath);
      setAnalysisData(data);
      if (data.diagnostic_report?.hardware_device) {
        setHardwareInfo(data.diagnostic_report.hardware_device);
      }
    } catch (err) {
      alert("Error analyzing dataset file: " + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleSampleSelect = async (scenarioId) => {
    setLoading(true);
    setActiveScenario(scenarioId);
    try {
      const data = await analyzeSampleScenario(scenarioId);
      setAnalysisData(data);
      if (data.diagnostic_report?.hardware_device) {
        setHardwareInfo(data.diagnostic_report.hardware_device);
      }
    } catch (err) {
      console.error("Error loading scenario:", err);
    } finally {
      setLoading(false);
    }
  };

  const mlPred = analysisData?.ml_prediction;
  const physicsSummary = analysisData?.physics_summary;
  const diagnosticReport = analysisData?.diagnostic_report;

  const fullDiagnosticContext = {
    ml_prediction: mlPred,
    physics_summary: physicsSummary,
    diagnostic_report: diagnosticReport,
    filename: activeScenario || analysisData?.filename || 'ECU Telemetry Stream',
    fault_type: activeScenario
  };

  return (
    <div className="min-h-screen bg-[#0d1117] text-gray-100 flex font-sans selection:bg-cyan-500 selection:text-white">
      {/* LEFT SIDEBAR NAVIGATION */}
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} hardwareInfo={hardwareInfo} />

      {/* MAIN RIGHT VIEWPORT WORKSPACE */}
      <div className="flex-1 flex flex-col min-w-0 h-screen overflow-y-auto">
        {/* Top Header Workspace Bar */}
        <header className="bg-[#161b22] border-b border-[#30363d] px-6 py-3.5 sticky top-0 z-40 flex items-center justify-between shadow-sm">
          <div className="flex items-center gap-3">
            <h2 className="text-base font-bold text-white tracking-wide uppercase font-mono">
              {activeTab === 'overview' && '1. Diagnostics & Telemetry Ingestion'}
              {activeTab === 'llm' && '2. RAG LLM Repair Report & Mechanic AI Chat'}
              {activeTab === 'digitaltwin' && '3. CAT C18 6-Cylinder Engine 3D Digital Twin'}
              {activeTab === 'schematic' && '4. Inline-6 Visual HUD & Cylinder Map'}
              {activeTab === 'physics' && '5. Physics Telemetry & PyTorch PINN Metrics'}
              {activeTab === 'chat' && '6. Interactive Mechanic AI Chat Assistant'}
              {activeTab === 'dataset' && '7. 5.0 GB Diesel ECU Dataset Workspace'}
            </h2>
          </div>

          <div className="flex items-center gap-3">
            {loading && (
              <span className="text-xs font-mono text-cyan-400 flex items-center gap-1.5 animate-pulse bg-cyan-500/10 px-3 py-1.5 rounded-lg border border-cyan-500/30">
                <RefreshCw className="w-3.5 h-3.5 animate-spin text-cyan-400" />
                <span>PINN Transformer Analyzing...</span>
              </span>
            )}

            <button
              onClick={() => setIsGeneratorOpen(true)}
              className="px-3 py-1.5 bg-cyan-600/20 hover:bg-cyan-600/30 text-cyan-300 border border-cyan-500/40 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors"
            >
              <span>Generator Tool</span>
            </button>
          </div>
        </header>

        {/* Page Content Viewport */}
        <main className="flex-1 p-6 space-y-6">
          {/* PAGE 1: OVERVIEW */}
          {activeTab === 'overview' && (
            <div className="space-y-6 max-w-7xl mx-auto">
              <TelemetryUploader
                onFileUpload={handleFileUpload}
                onDatasetFileSelect={handleDatasetFileSelect}
                onSampleSelect={handleSampleSelect}
                onLiveStreamUpdate={handleLiveStreamUpdate}
                isLoading={loading}
                activeScenario={activeScenario}
              />

              {mlPred && (
                <>
                  <DiagnosticCard mlPrediction={mlPred} />
                  <LiveTelemetrySheet 
                    telemetryPreview={analysisData?.telemetry_preview}
                    latestSensors={analysisData?.telemetry_preview ? analysisData.telemetry_preview[analysisData.telemetry_preview.length - 1] : null} 
                    physicsSummary={physicsSummary}
                    mlPrediction={mlPred}
                  />
                </>
              )}

            </div>
          )}

          {/* PAGE 2: RAG LLM REPAIR REPORT WITH MECHANIC CHAT DIRECTLY UNDERNEATH */}
          {activeTab === 'llm' && (
            <div className="space-y-6 max-w-5xl mx-auto">
              <LLMReportView diagnosticReport={diagnosticReport} />
              
              <div className="border-t border-[#30363d] pt-6">
                <h3 className="text-sm font-bold text-white mb-3 flex items-center gap-2">
                  <MessageSquare className="w-4 h-4 text-cyan-400" />
                  Interactive Mechanic AI Diagnostic Chat Assistant
                </h3>
                <InteractiveChat diagnosticContext={fullDiagnosticContext} />
              </div>
            </div>
          )}

          {/* PAGE 3: 3D DIGITAL TWIN VIEWER */}
          {activeTab === 'digitaltwin' && (
            <DigitalTwinView />
          )}

          {/* PAGE 4: ENGINE VISUAL SCHEMATIC HUD */}
          {activeTab === 'schematic' && (
            <div className="space-y-6 max-w-7xl mx-auto">
              <div className="bg-[#161b22] border border-[#30363d] p-4 rounded-xl flex items-center justify-between">
                <div>
                  <h3 className="text-sm font-bold text-white flex items-center gap-2">
                    <Activity className="w-4 h-4 text-cyan-400" />
                    Inline-6 Diesel Engine Real-Time Visual Schematic
                  </h3>
                  <p className="text-xs text-gray-400 mt-0.5">
                    Visual mechanical diagram showing Cylinders 1-6 power indices, Common Rail fuel lines, VGT turbo, and EGR valves.
                  </p>
                </div>
              </div>
              <EngineSchematicI6 mlPrediction={mlPred} physicsSummary={physicsSummary} />
            </div>
          )}

          {/* PAGE 5: PHYSICS & PINN METRICS DEEP-DIVE */}
          {activeTab === 'physics' && (
            <div className="space-y-6 max-w-7xl mx-auto">
              <div className="bg-[#161b22] border border-[#30363d] p-4 rounded-xl flex items-center justify-between">
                <div>
                  <h3 className="text-sm font-bold text-white flex items-center gap-2">
                    <BarChart3 className="w-4 h-4 text-cyan-400" />
                    Physics Telemetry Residuals & PyTorch PINN Transformer Output
                  </h3>
                  <p className="text-xs text-gray-400 mt-0.5">
                    Analytical ideal gas airflow residuals, lean lambda bank variance, dynamic crank acceleration balance (CPI 1 to 6).
                  </p>
                </div>
              </div>
              <PhysicsTelemetryCharts physicsSummary={physicsSummary} />
            </div>
          )}

          {/* PAGE 6: MECHANIC AI CHAT */}
          {activeTab === 'chat' && (
            <div className="max-w-5xl mx-auto">
              <InteractiveChat diagnosticContext={fullDiagnosticContext} />
            </div>
          )}

          {/* PAGE 7: 5GB DATASET MANAGER */}
          {activeTab === 'dataset' && (
            <div className="max-w-7xl mx-auto">
              <DatasetManagerPage onSelectDatasetFile={handleDatasetFileSelect} isLoading={loading} />
            </div>
          )}
        </main>

        <footer className="border-t border-[#30363d] bg-[#161b22] py-3.5 text-center text-xs text-gray-500 mt-auto">
          Diesel Inline-6 Engine LLM Diagnostic Suite • PyTorch PINN & NVIDIA GPU CUDA Active
        </footer>
      </div>

      <SyntheticGeneratorModal
        isOpen={isGeneratorOpen}
        onClose={() => setIsGeneratorOpen(false)}
      />
    </div>
  );
}
