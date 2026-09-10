# I6 Engine Diagnostic System - Standalone Frontend UI

This folder contains the complete, self-contained frontend application for the **6-Cylinder Inline Engine Diagnostic Dashboard**.

## 📁 Directory Overview

- **`src/`**: React application components (Telemetry uploader, I6 interactive schematic visualizer, diagnostic reports, physics charts, live telemetry sheet, mechanic AI chat).
- **`public/3d-viewer/`**: Embedded Three.js WebGL 3D Digital Twin viewer assets & 117MB `c18.glb` engine CAD model.
- **`3d-viewer/`**: Source code for the 3D WebGL CAD viewer (Three.js, OrbitControls, GLTFLoader).
- **`vite.config.js`**: Vite configuration with `/api` reverse proxying to `http://127.0.0.1:8000`.

---

## 🚀 How to Run (Frontend Only)

### 1. Install Dependencies
```bash
npm install
```

### 2. Start Development Server
```bash
npm run dev
```

Open your browser at `http://localhost:3000`.

---

## 🔗 Backend API Connection

The frontend expects the FastAPI backend running at `http://127.0.0.1:8000`. 
All API requests (`/api/*`) are automatically proxied via `vite.config.js`.

To start the backend in the backend folder:
```bash
cd ../backend
python -m uvicorn app.main:app --reload --port 8000
```

