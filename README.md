# LLM-Centric 6-Cylinder Inline Engine Diagnostic System

An advanced, highly accurate automotive diagnostic engine tailored specifically for **6-Cylinder Inline (I6)** engines.

The system combines:
1. **Physics-Informed Modeling**: I6 crankshaft angular velocity dynamics ($120^\circ$ firing order stroke balance: 1-5-3-6-2-4), Cylinder Power Index ($CPI_{1..6}$), Orifice airflow theoretical mass balance, and Stoichiometric bank balance.
2. **Machine Learning Classifier**: Multi-class XGBoost + Random Forest ensemble trained on physics metrics with Platt-scaled confidence scores ($0-100\%$).
3. **RAG + Hugging Face LLM Engine**: Retrieval-Augmented Generation using ChromaDB vector store seeded with OEM service manuals, bolt torque specs, and SAE fault trees.
4. **NVIDIA GPU Ready Architecture**: Auto-detects PyTorch CUDA acceleration and interfaces with local Hugging Face transformer models / vLLM / TensorRT endpoints.
5. **Modern React Web Dashboard**: Interactive 2D visual schematic of the 6-Cylinder Inline engine highlighting affected cylinders/components in real-time, physics telemetry tables, LLM diagnostic reports, interactive chat, and a synthetic ECU log generator.

---

## Required 4 Core System Outputs

For any uploaded ECU CSV/Excel file or synthetic scenario, the system provides:
1. **Issue / No Issue Status**: Clear binary status badge (`ISSUE DETECTED` vs `NO ISSUE`).
2. **Exact Isolated Location**: Specific component or cylinder (e.g. `Cylinder 3 (Ignition / Combustion Chamber)` or `Intake Charge Air Tract (Post-Compressor Boost Leak)`).
3. **Model Confidence Score (%)**: Calibrated confidence metric (e.g. `96.4%`).
4. **LLM Diagnostic & OEM Repair Recommendation**: Actionable root cause analysis, thermodynamic explanation, step-by-step physical inspection workflow, and bolt torque specifications.

---

## Project Structure

```
d:/LLM Forge/
├── backend/
│   ├── app/
│   │   ├── config.py                  # PyTorch CUDA GPU auto-detection & settings
│   │   ├── main.py                    # FastAPI application entrypoint
│   │   ├── engine_physics/
│   │   │   ├── i6_kinematics.py       # I6 Crank torque & CPI_1..6 calculation
│   │   │   ├── thermodynamics.py      # Mass airflow, Boost ratio, Bank Lambda balance
│   │   │   └── feature_extractor.py   # Unified physics residual feature extractor
│   │   ├── ml_models/
│   │   │   ├── classifier.py          # XGBoost + RF ensemble with Platt scaling
│   │   │   └── synthetic_generator.py # ECU CSV log simulator (8 fault modes)
│   │   ├── rag/
│   │   │   ├── vector_store.py        # SentenceTransformers / ChromaDB vector search
│   │   │   ├── knowledge_base/        # OEM I6 manuals & SAE fault trees JSON
│   │   │   └── llm_diagnostic_engine.py# Hugging Face LLM diagnostic report generator
│   │   └── api/
│   │       ├── routes_analyze.py      # ECU file upload & sample analysis
│   │       ├── routes_generator.py    # Synthetic CSV download endpoint
│   │       └── routes_chat.py         # Interactive Q&A chat endpoint
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx             # System & GPU status header
│   │   │   ├── TelemetryUploader.jsx  # Drag-and-drop CSV/Excel uploader & presets
│   │   │   ├── EngineSchematicI6.jsx  # Interactive visual I6 cylinder layout
│   │   │   ├── DiagnosticCard.jsx     # Summary card for 4 requested outputs
│   │   │   ├── PhysicsTelemetryCharts.jsx # Physics metrics table
│   │   │   ├── LLMReportView.jsx      # Formatted Markdown LLM report
│   │   │   ├── InteractiveChat.jsx    # Interactive Mechanic Q&A chat
│   │   │   └── SyntheticGeneratorModal.jsx # ECU log generator tool
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
└── README.md
```

---

## How to Run

### 1. Start FastAPI Backend (Port 8000)
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```
API Documentation will be available at `http://127.0.0.1:8000/docs`.

### 2. Start Standalone Frontend (Port 3000)
```bash
cd frontend
npm run dev
```
Open your browser at `http://localhost:3000`. (The 3D Digital Twin WebGL Viewer is embedded directly in the frontend application).

---

## Deploying on NVIDIA GPU

1. Ensure NVIDIA CUDA Drivers and PyTorch with CUDA support are installed:
   ```bash
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
   ```
2. Set environment variable for Hugging Face GPU model:
   ```bash
   export HF_MODEL_NAME="Qwen/Qwen2.5-Coder-1.5B-Instruct"
   ```
3. The system will automatically detect the GPU device (`cuda:0`) and utilize hardware acceleration for both vector embeddings and LLM inference.
