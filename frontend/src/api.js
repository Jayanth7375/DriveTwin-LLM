import axios from 'axios';

const API_BASE = '/api';

export const uploadEcuFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await axios.post(`${API_BASE}/analyze`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

export const analyzeSampleScenario = async (faultType) => {
  const response = await axios.post(`${API_BASE}/analyze-sample`, {
    fault_type: faultType,
  });
  return response.data;
};

export const fetchAvailableFaults = async () => {
  const response = await axios.get(`${API_BASE}/fault-types`);
  return response.data;
};

export const fetchDatasetFiles = async () => {
  const response = await axios.get(`${API_BASE}/dataset-files`);
  return response.data;
};

export const analyzeDatasetFile = async (relativePath) => {
  const response = await axios.post(`${API_BASE}/analyze-dataset-file`, {
    relative_path: relativePath,
  });
  return response.data;
};

// --- LIVE ECU HARDWARE HARDWARE API ---
export const fetchEcuComPorts = async () => {
  const response = await axios.get(`${API_BASE}/ecu-live/ports`);
  return response.data;
};

export const connectLiveEcu = async (config) => {
  const response = await axios.post(`${API_BASE}/ecu-live/connect`, config);
  return response.data;
};

export const disconnectLiveEcu = async () => {
  const response = await axios.post(`${API_BASE}/ecu-live/disconnect`);
  return response.data;
};

export const fetchLiveTelemetryStream = async () => {
  const response = await axios.get(`${API_BASE}/ecu-live/telemetry-stream`);
  return response.data;
};

export const downloadSyntheticCsvUrl = (faultType) => {
  return `${API_BASE}/generate-csv`;
};

export const sendChatMessage = async (message, diagnosticContext, history) => {
  const response = await axios.post(`${API_BASE}/chat`, {
    message,
    diagnostic_context: diagnosticContext,
    history,
  });
  return response.data;
};
