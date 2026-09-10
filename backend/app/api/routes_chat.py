from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from ..rag.llm_diagnostic_engine import LLMDiagnosticEngine

router = APIRouter(prefix="/api", tags=["Chat"])
llm_engine = LLMDiagnosticEngine()

class ChatMessageRequest(BaseModel):
    message: str
    diagnostic_context: Optional[Dict[str, Any]] = None
    history: Optional[List[Dict[str, Any]]] = None

@router.post("/chat")
def chat_with_llm(req: ChatMessageRequest):
    """
    Handles stateful interactive follow-up Q&A regarding active dashboard ECU telemetry,
    step-by-step diagnostic workflows, OEM torque specs, and RAG knowledge base manuals.
    """
    try:
        context = req.diagnostic_context or {}
        history = req.history or []
        answer = llm_engine.chat_answer(req.message, context, history)
        return {
            "status": "success",
            "reply": answer
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat Error: {str(e)}")
