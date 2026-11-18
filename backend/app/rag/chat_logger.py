import os
import json
import time
import uuid
import re
from typing import Dict, Any, List, Optional

LOG_DIR = os.path.join(os.path.dirname(__file__), "chat_logs")
LOG_FILE = os.path.join(LOG_DIR, "chat_feedback_dataset.jsonl")

class ChatScorerAndLogger:
    """
    Automated Chat Scoring, Quality Evaluation & Dataset Logger.
    Logs all user interactions, computes automated quality/relevance scores,
    and records user feedback (thumbs up/down) for future LLM fine-tuning (DPO/RLHF).
    """
    def __init__(self):
        os.makedirs(LOG_DIR, exist_ok=True)

    def calculate_automated_score(
        self,
        user_query: str,
        llm_reply: str,
        context: Dict[str, Any]
    ) -> Dict[str, float]:
        """
        Calculates automated quality heuristics (0.0 to 1.0) for the response.
        """
        # 1. Structure Score (Tables, bold headings, code blocks)
        has_table = "|" in llm_reply and "---" in llm_reply
        has_headers = "###" in llm_reply or "####" in llm_reply or "**" in llm_reply
        has_code = "`" in llm_reply
        structure_score = (0.4 if has_table else 0.0) + (0.3 if has_headers else 0.0) + (0.3 if has_code else 0.0)

        # 2. Context Alignment Score
        fault_code = context.get("fault_code", "")
        location = context.get("isolated_location", "")
        alignment_score = 0.5
        if fault_code and fault_code in llm_reply:
            alignment_score += 0.25
        if location and location in llm_reply:
            alignment_score += 0.25

        # 3. Overall Combined Automated Quality Score
        composite_score = round(0.5 * structure_score + 0.5 * alignment_score, 3)

        return {
            "composite_score": composite_score,
            "structure_score": round(structure_score, 2),
            "alignment_score": round(alignment_score, 2)
        }

    def log_interaction(
        self,
        user_query: str,
        llm_reply: str,
        context: Dict[str, Any],
        session_id: Optional[str] = None
    ) -> str:
        """
        Logs a chat interaction with automated quality scoring.
        Returns unique interaction ID.
        """
        interaction_id = str(uuid.uuid4())
        scores = self.calculate_automated_score(user_query, llm_reply, context)

        log_entry = {
            "interaction_id": interaction_id,
            "session_id": session_id or interaction_id,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "user_query": user_query,
            "llm_reply": llm_reply,
            "context": {
                "fault_code": context.get("fault_code"),
                "isolated_location": context.get("isolated_location"),
                "severity": context.get("severity")
            },
            "automated_scores": scores,
            "user_feedback": None  # Will be populated via POST /api/chat/feedback
        }

        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")

        return interaction_id

    def record_user_feedback(self, interaction_id: str, feedback_score: float, comment: Optional[str] = None) -> bool:
        """
        Updates user feedback (1.0 for thumbs up, 0.0 for thumbs down).
        """
        if not os.path.exists(LOG_FILE):
            return False

        updated = False
        rows = []

        with open(LOG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                data = json.loads(line)
                if data.get("interaction_id") == interaction_id:
                    data["user_feedback"] = {
                        "rating": feedback_score,  # 1.0 = Thumbs Up, 0.0 = Thumbs Down
                        "comment": comment,
                        "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    updated = True
                rows.append(data)

        if updated:
            with open(LOG_FILE, "w", encoding="utf-8") as f:
                for row in rows:
                    f.write(json.dumps(row) + "\n")

        return updated
