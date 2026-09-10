import os
import io
import pandas as pd
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from ..ml_models.synthetic_generator import ECUSyntheticGenerator
from ..engine_physics.feature_extractor import PhysicsFeatureExtractor
from ..ml_models.classifier import EngineFaultClassifier
from ..ml_models.pinn_transformer import PINNTrainerWrapper
from ..rag.llm_diagnostic_engine import LLMDiagnosticEngine

router = APIRouter(prefix="/api", tags=["Synthetic Generator & Dataset"])

generator = ECUSyntheticGenerator()
feature_extractor = PhysicsFeatureExtractor()
classifier = EngineFaultClassifier()
pinn_engine = PINNTrainerWrapper()
llm_engine = LLMDiagnosticEngine()

class GeneratorRequest(BaseModel):
    fault_type: str = "NO_ISSUE"
    num_samples: int = 300

class SelectDatasetFileRequest(BaseModel):
    relative_path: str

@router.get("/fault-types")
def get_available_fault_types():
    return generator.FAULT_TYPES

@router.post("/generate-csv")
def generate_ecu_csv(req: GeneratorRequest):
    try:
        df = generator.generate(fault_type=req.fault_type, num_samples=req.num_samples)
        csv_content = df.to_csv(index=False)
        filename = f"ecu_log_{req.fault_type.lower()}_i6.csv"
        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation Error: {str(e)}")

@router.get("/dataset-files")
def list_dataset_files():
    """
    Lists files available in d:/LLM Forge/dataset_5gb for 1-click selection in the Web UI.
    """
    base_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "dataset_5gb")
    base_dir = os.path.abspath(base_dir)
    
    if not os.path.exists(base_dir):
        return {"files": [], "total_count": 0, "message": "Dataset directory not generated yet"}
        
    categories = {}
    total_count = 0
    
    for root, dirs, files in os.walk(base_dir):
        csv_files = [f for f in files if f.endswith(".csv") or f.endswith(".xlsx")]
        if csv_files:
            rel_dir = os.path.relpath(root, base_dir)
            categories[rel_dir] = csv_files[:15]  # Show top 15 sample files per category
            total_count += len(csv_files)
            
    return {
        "categories": categories,
        "total_count": total_count,
        "base_dir": base_dir
    }

@router.post("/analyze-dataset-file")
def analyze_dataset_file_by_path(req: SelectDatasetFileRequest):
    """
    Analyzes a specific file from dataset_5gb.
    """
    try:
        base_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "dataset_5gb")
        target_path = os.path.abspath(os.path.join(base_dir, req.relative_path))
        
        if not os.path.exists(target_path):
            raise HTTPException(status_code=404, detail="Selected dataset file not found.")
            
        if target_path.endswith(".csv"):
            df = pd.read_csv(target_path)
        else:
            df = pd.read_excel(target_path)
            
        pinn_result = pinn_engine.predict_sequence(df)
        physics_summary, feature_vector = feature_extractor.extract(df)
        ml_pred = classifier.predict(feature_vector)
        ml_pred["pinn_transformer"] = pinn_result
        
        report = llm_engine.generate_diagnostic_report(ml_pred, physics_summary)
        preview_df = df.iloc[::100].to_dict(orient="records")
        
        return {
            "status": "success",
            "filename": os.path.basename(target_path),
            "row_count": len(df),
            "ml_prediction": ml_pred,
            "physics_summary": physics_summary,
            "diagnostic_report": report,
            "telemetry_preview": preview_df
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dataset File Analysis Error: {str(e)}")
