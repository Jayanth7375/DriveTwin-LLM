import os
import json
from app.rag.chat_logger import LOG_FILE

OUTPUT_SFT = "d:/LLM Forge/backend/app/rag/chat_logs/llm_instruction_tuning_dataset.jsonl"
OUTPUT_DPO = "d:/LLM Forge/backend/app/rag/chat_logs/llm_dpo_preference_dataset.jsonl"

def export_dataset():
    print("=" * 70)
    print("    EXPORTING LLM CHAT SCORED DATASET FOR FUTURE FINE-TUNING")
    print("=" * 70)

    if not os.path.exists(LOG_FILE):
        print(f"No chat dataset found at '{LOG_FILE}'. Log some chat sessions first!")
        return

    sft_records = []
    dpo_records = []

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            data = json.loads(line)
            query = data.get("user_query")
            reply = data.get("llm_reply")
            scores = data.get("automated_scores", {})
            comp_score = scores.get("composite_score", 0.0)
            user_fb = data.get("user_feedback")

            # Filter high-quality pairs (composite score >= 0.70 or thumbs up user rating = 1.0)
            is_high_quality = comp_score >= 0.70 or (user_fb and user_fb.get("rating") == 1.0)

            if is_high_quality:
                sft_records.append({
                    "instruction": query,
                    "system_prompt": "You are a domain-trained Driver Care & Automotive Diagnostic AI Assistant.",
                    "response": reply,
                    "score": comp_score
                })

            # DPO preference data (if feedback given)
            if user_fb and "rating" in user_fb:
                rating = user_fb["rating"]
                if rating == 1.0:
                    dpo_records.append({
                        "prompt": query,
                        "chosen": reply,
                        "rejected": "Generic short response without diagnostic details."
                    })

    # Save SFT JSONL
    with open(OUTPUT_SFT, "w", encoding="utf-8") as f:
        for r in sft_records:
            f.write(json.dumps(r) + "\n")

    # Save DPO JSONL
    with open(OUTPUT_DPO, "w", encoding="utf-8") as f:
        for r in dpo_records:
            f.write(json.dumps(r) + "\n")

    print(f"Exported {len(sft_records)} High-Quality Instruction Tuning pairs to:\n  -> {os.path.abspath(OUTPUT_SFT)}")
    print(f"Exported {len(dpo_records)} DPO Preference pairs to:\n  -> {os.path.abspath(OUTPUT_DPO)}")
    print("=" * 70)

if __name__ == "__main__":
    export_dataset()
