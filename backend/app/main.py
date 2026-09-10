import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import settings
from .api import routes_analyze, routes_generator, routes_chat, routes_ecu_live

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="LLM-Centric 6-Cylinder Inline Engine Diagnostic & Physics Analysis API"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_analyze.router)
app.include_router(routes_generator.router)
app.include_router(routes_chat.router)
app.include_router(routes_ecu_live.router)

@app.get("/")
def root():
    return {
        "system": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "engine_target": settings.ENGINE.layout,
        "firing_order": settings.ENGINE.firing_order,
        "hardware_device": settings.DEVICE,
        "gpu_name": settings.GPU_NAME,
        "hf_model": settings.HF_MODEL_NAME,
        "status": "ONLINE"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
