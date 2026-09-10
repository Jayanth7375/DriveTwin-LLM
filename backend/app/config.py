import os
import torch
from pydantic import BaseModel

class EngineSpecs(BaseModel):
    num_cylinders: int = 6
    layout: str = "Diesel Inline-6 (I6)"
    firing_order: list[int] = [1, 5, 3, 6, 2, 4]
    displacement_liters: float = 6.7  # 6.7L Diesel I6 Platform
    idle_rpm: float = 700.0
    max_rpm: float = 4500.0
    stoich_afr: float = 14.5  # Diesel Stoichiometry (Operates lean Lambda 1.2 to 2.5)
    fuel_type: str = "Diesel"

class Settings:
    PROJECT_NAME: str = "I6 Engine Diagnostic & Analysis System"
    VERSION: str = "1.0.0"
    
    # Engine Physics Parameters
    ENGINE: EngineSpecs = EngineSpecs()
    
    # GPU / Hardware Acceleration Setup
    DEVICE: str = "cuda" if torch.cuda.is_available() else "cpu"
    GPU_NAME: str = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU Execution"
    
    # Hugging Face LLM & Embedding Models
    HF_MODEL_NAME: str = os.getenv("HF_MODEL_NAME", "Qwen/Qwen2.5-Coder-1.5B-Instruct")
    HF_FALLBACK_MODEL: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Vector DB Storage
    VECTOR_DB_DIR: str = os.path.join(os.path.dirname(__file__), "rag", "vector_data")
    
settings = Settings()
