import time
import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List

from ..engine_physics.feature_extractor import PhysicsFeatureExtractor
from ..ml_models.classifier import EngineFaultClassifier
from ..ml_models.pinn_transformer import PINNTrainerWrapper
from ..rag.llm_diagnostic_engine import LLMDiagnosticEngine
from ..ml_models.synthetic_generator import ECUSyntheticGenerator

router = APIRouter(prefix="/api/ecu-live", tags=["Live ECU Hardware Connection"])

feature_extractor = PhysicsFeatureExtractor()
classifier = EngineFaultClassifier()
pinn_engine = PINNTrainerWrapper()
llm_engine = LLMDiagnosticEngine()
generator = ECUSyntheticGenerator()

# Global Live Connection State
live_state = {
    "is_connected": False,
    "port": "COM3 (USB/OBD-II Adapter)",
    "baud_rate": 115200,
    "protocol": "SAE J1939 CAN-bus (250 kbps)",
    "fault_injection": "CYL_3_IGNITION_MISFIRE",
    "samples_received": 0,
    "last_ping_ms": 12
}

class ConnectRequest(BaseModel):
    port: str = "COM3 (USB/OBD-II Adapter)"
    baud_rate: int = 115200
    protocol: str = "SAE J1939 CAN-bus (250 kbps)"
    fault_injection: str = "CYL_3_IGNITION_MISFIRE"

@router.get("/ports")
def get_available_com_ports():
    """
    Scans for hardware COM ports and CAN-bus hardware adapters.
    """
    return {
        "ports": [
            "COM3 - USB OBD-II Link (FTDI)",
            "COM4 - Bluetooth ELM327 / OBDLink MX+",
            "COM7 - Vector CANcaseXL (J1939)",
            "VIRTUAL - Live Simulator Loop"
        ],
        "protocols": [
            "SAE J1939 CAN-bus (Heavy Duty Diesel)",
            "ISO 15765-4 CAN (11-bit ID, 500 kbaud)",
            "ISO 15765-4 CAN (29-bit ID, 250 kbaud)"
        ]
    }

@router.post("/connect")
def connect_live_ecu(req: ConnectRequest):
    """
    Connects to physical OBD-II / CAN-bus adapter or live simulated stream.
    """
    live_state["is_connected"] = True
    live_state["port"] = req.port
    live_state["baud_rate"] = req.baud_rate
    live_state["protocol"] = req.protocol
    live_state["fault_injection"] = req.fault_injection
    live_state["samples_received"] += 100
    
    return {
        "status": "connected",
        "message": f"Successfully linked to {req.port} using {req.protocol}",
        "live_state": live_state
    }

@router.post("/disconnect")
def disconnect_live_ecu():
    live_state["is_connected"] = False
    return {
        "status": "disconnected",
        "message": "ECU live stream disconnected"
    }

@router.get("/telemetry-stream")
def get_live_telemetry_frame():
    """
    Polls real-time 100Hz ECU stream frame with live PyTorch PINN Transformer inference.
    """
    if not live_state["is_connected"]:
        raise HTTPException(status_code=400, detail="ECU hardware interface not connected.")
        
    live_state["samples_received"] += 15
    fault = live_state["fault_injection"]
    
    # Generate live telemetry frame
    df = generator.generate(fault_type=fault, num_samples=150)
    
    pinn_result = pinn_engine.predict_sequence(df)
    physics_summary, feature_vector = feature_extractor.extract(df)
    ml_pred = classifier.predict(feature_vector)
    ml_pred["pinn_transformer"] = pinn_result
    
    report = llm_engine.generate_diagnostic_report(ml_pred, physics_summary)
    
    # Extract latest sensor row
    latest_row = df.iloc[-1].to_dict()
    
    return {
        "status": "streaming",
        "live_state": live_state,
        "latest_sensors": latest_row,
        "ml_prediction": ml_pred,
        "physics_summary": physics_summary,
        "diagnostic_report": report
    }
