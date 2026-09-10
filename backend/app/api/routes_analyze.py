import io
import pandas as pd
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional

from ..engine_physics.feature_extractor import PhysicsFeatureExtractor
from ..ml_models.classifier import EngineFaultClassifier
from ..ml_models.pinn_transformer import PINNTrainerWrapper
from ..rag.llm_diagnostic_engine import LLMDiagnosticEngine
from ..ml_models.synthetic_generator import ECUSyntheticGenerator

router = APIRouter(prefix="/api", tags=["Analysis"])

feature_extractor = PhysicsFeatureExtractor()
classifier = EngineFaultClassifier()
pinn_engine = PINNTrainerWrapper()
llm_engine = LLMDiagnosticEngine()
synthetic_gen = ECUSyntheticGenerator()

class SampleAnalyzeRequest(BaseModel):
    fault_type: str = "CYL_3_IGNITION_MISFIRE"

@router.post("/analyze")
async def analyze_ecu_file(file: UploadFile = File(...)):
    """
    Upload ECU telemetry CSV or Excel file for PINN Transformer + Physics + LLM analysis.
    """
    try:
        content = await file.read()
        filename = file.filename.lower()
        
        if filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(content))
        elif filename.endswith(".xlsx") or filename.endswith(".xls"):
            df = pd.read_excel(io.BytesIO(content))
        else:
            raise HTTPException(status_code=400, detail="Invalid file format. Upload CSV or Excel (.xlsx).")
            
        if df.empty:
            raise HTTPException(status_code=400, detail="Uploaded file contains no telemetry data rows.")

        # 1. Custom PyTorch PINN Telemetry Transformer Inference (Built from scratch)
        pinn_result = pinn_engine.predict_sequence(df)

        # 2. Physics Feature Extraction
        physics_summary, feature_vector = feature_extractor.extract(df)
        
        # 3. Ensemble Machine Learning Classification
        ml_pred = classifier.predict(feature_vector)
        
        # Enrich ML prediction with PINN PyTorch Transformer output
        ml_pred["pinn_transformer"] = pinn_result

        # 4. RAG LLM Diagnostic Report Generation
        report = llm_engine.generate_diagnostic_report(ml_pred, physics_summary)
        
        # 5. Extract timeline rows for frontend dynamic playback
        step = max(1, len(df) // 200)
        preview_df = df.iloc[::step].to_dict(orient="records")
        
        return {
            "status": "success",
            "filename": file.filename,
            "row_count": len(df),
            "ml_prediction": ml_pred,
            "physics_summary": physics_summary,
            "diagnostic_report": report,
            "telemetry_preview": preview_df
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ECU Analysis Error: {str(e)}")


@router.post("/analyze-sample")
async def analyze_sample_ecu(req: SampleAnalyzeRequest):
    """
    Runs full PINN Transformer + Physics + LLM diagnostic pipeline on sample ECU scenario.
    """
    try:
        df = synthetic_gen.generate(fault_type=req.fault_type, num_samples=300)
        
        pinn_result = pinn_engine.predict_sequence(df)
        physics_summary, feature_vector = feature_extractor.extract(df)
        ml_pred = classifier.predict(feature_vector)
        ml_pred["pinn_transformer"] = pinn_result
        
        report = llm_engine.generate_diagnostic_report(ml_pred, physics_summary)
        
        preview_df = df.iloc[::5].to_dict(orient="records")
        
        return {
            "status": "success",
            "fault_type": req.fault_type,
            "row_count": len(df),
            "ml_prediction": ml_pred,
            "physics_summary": physics_summary,
            "diagnostic_report": report,
            "telemetry_preview": preview_df
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sample Analysis Error: {str(e)}")

@router.post("/retrain-pinn")
async def retrain_pinn_model(epochs: int = 25):
    """
    Retrains the PyTorch PINN Telemetry Transformer model on synthetic Diesel timelines
    mapped to SAE J1939 fault codes and OEM troubleshooting manual specifications.
    """
    try:
        res = pinn_engine.train_pinn_from_scratch(epochs=epochs)
        return {
            "status": "success",
            "message": f"PyTorch PINN Telemetry Transformer retrained successfully for {epochs} epochs.",
            "details": res
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retraining Error: {str(e)}")

