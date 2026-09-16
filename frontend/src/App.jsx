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
import VideoLanding from './components/VideoLanding';
import LiveTelemetrySheet from './components/LiveTelemetrySheet';
import { uploadEcuFile, analyzeSampleScenario, analyzeDatasetFile } from './api';
import { RefreshCw } from 'lucide-react';

export default function App() {
  const [showLanding, setShowLanding] = useState(true);
  const [activeTab, setActiveTab] = useState('overview'); 
  const [analysisData, setAnalysisData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeScenario, setActiveScenario] = useState('CYL_3_IGNITION_MISFIRE');
  const [isGeneratorOpen, setIsGeneratorOpen] = useState(false);
  const [hardwareInfo, setHardwareInfo] = useState('');
  
  // UI States
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(true);

  // Apply dark mode class to html element
  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDarkMode]);

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

  if (showLanding) {
    return <VideoLanding onEnter={() => setShowLanding(false)} />;
  }

  return (
    <div className={`min-h-screen flex font-sans selection:bg-cyan-500 selection:text-white transition-colors duration-300 ${isDarkMode ? 'bg-[#0d1117] text-gray-100' : 'bg-gray-50 bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(34,211,238,0.15),rgba(255,255,255,0))] text-gray-900'}`}>
      {/* LEFT SIDEBAR NAVIGATION */}
      <Sidebar 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
        hardwareInfo={hardwareInfo}
        isCollapsed={isSidebarCollapsed}
        setIsCollapsed={setIsSidebarCollapsed}
        isDarkMode={isDarkMode}
        setIsDarkMode={setIsDarkMode}
      />

      {/* MAIN RIGHT VIEWPORT WORKSPACE */}
      <div className="flex-1 flex flex-col min-w-0 h-screen overflow-y-auto">
        {/* Top Header Workspace Bar */}
        <header className={`px-6 py-3.5 sticky top-0 z-40 flex items-center justify-between shadow-sm border-b transition-colors duration-300 ${isDarkMode ? 'bg-[#161b22]/80 backdrop-blur-xl border-white/10' : 'bg-white/80 backdrop-blur-xl border-gray-200/50'}`}>
          <div className="flex items-center gap-3">
            <h2 className={`text-base font-bold tracking-wide uppercase font-mono ${isDarkMode ? 'text-white' : 'text-gray-800'}`}>
              {activeTab === 'overview' && '1. Diagnostics & Telemetry Ingestion'}
              {activeTab === 'llm' && '2. RAG LLM Repair Report & Mechanic AI Chat'}
              {activeTab === 'digitaltwin' && '3. CAT C18 6-Cylinder Engine 3D Digital Twin'}
              {activeTab === 'schematic' && 'Real-Time Engine Monitoring'}
              {activeTab === 'physics' && '5. Physics Telemetry & PyTorch PINN Metrics'}
              {activeTab === 'chat' && '6. Interactive Mechanic AI Chat Assistant'}
              {activeTab === 'dataset' && '7. 5.0 GB Diesel ECU Dataset Workspace'}
            </h2>
          </div>

          <div className="flex items-center gap-3">
            {loading && (
              <span className={`text-xs font-mono flex items-center gap-1.5 px-3 py-1.5 rounded-lg border animate-pulse ${isDarkMode ? 'bg-cyan-500/10 border-cyan-500/30 text-cyan-400' : 'bg-cyan-50 border-cyan-200 text-cyan-700'}`}>
                <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                <span>PINN Transformer Analyzing...</span>
              </span>
            )}

            <button
              onClick={() => setIsGeneratorOpen(true)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors border ${isDarkMode ? 'bg-cyan-600/20 hover:bg-cyan-600/30 text-cyan-300 border-cyan-500/40' : 'bg-cyan-50 hover:bg-cyan-100 text-cyan-700 border-cyan-200'}`}
            >
              <span>Generator Tool</span>
            </button>
          </div>
        </header>

        {/* Page Content Viewport */}
        <main className="flex-1 p-6 space-y-6">
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

          {activeTab === 'llm' && (
            <div className="space-y-6 w-full">
              <LLMReportView diagnosticReport={diagnosticReport} />
              <div className={`border-t pt-6 ${isDarkMode ? 'border-[#30363d]' : 'border-gray-200'}`}>
                <h3 className={`text-sm font-bold mb-3 flex items-center gap-2 ${isDarkMode ? 'text-white' : 'text-gray-800'}`}>
                  Interactive Mechanic AI Diagnostic Chat Assistant
                </h3>
                <InteractiveChat diagnosticContext={fullDiagnosticContext} />
              </div>
            </div>
          )}

          {activeTab === 'digitaltwin' && (
            <DigitalTwinView />
          )}

          {activeTab === 'schematic' && (
            <div className="max-w-7xl mx-auto">
              <EngineSchematicI6 mlPrediction={mlPred} physicsSummary={physicsSummary} />
            </div>
          )}

          {activeTab === 'physics' && (
            <div className="max-w-7xl mx-auto">
              <PhysicsTelemetryCharts physicsSummary={physicsSummary} mlPrediction={mlPred} />
            </div>
          )}

          {activeTab === 'chat' && (
            <div className="w-full">
              <InteractiveChat diagnosticContext={fullDiagnosticContext} />
            </div>
          )}

          {activeTab === 'dataset' && (
            <div className="max-w-7xl mx-auto">
              <DatasetManagerPage onSelectDatasetFile={handleDatasetFileSelect} isLoading={loading} />
            </div>
          )}
        </main>

        <footer className={`border-t py-3.5 text-center text-xs mt-auto transition-colors duration-300 ${isDarkMode ? 'bg-[#161b22]/80 backdrop-blur-xl border-white/10 text-gray-500' : 'bg-white/80 backdrop-blur-xl border-gray-200/50 text-gray-400'}`}>
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

