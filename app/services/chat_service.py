from core.prompt_engine import build_prompt
from core.model_router import call_model
from services.memory_service import add_message, get_history
import time
import traceback


# =========================
# CORE CHAT HANDLER
# =========================
def handle_chat(req):
    start_time = time.time()

    user_id = getattr(req, "user_id", "default")
    message = (req.message or "").strip()

    if not message:
        return {
            "reply": "Empty message not allowed",
            "intent": "ERROR",
            "latency": 0
        }

    try:
        # =========================
        # 1. STORE USER MESSAGE
        # =========================
        add_message(user_id, "user", message)

        # =========================
        # 2. LOAD HISTORY
        # =========================
        history = get_history(user_id) or []

        # =========================
        # 3. BUILD PROMPT
        # =========================
        prompt = build_prompt(message, history)

        # =========================
        # 4. CALL MODEL LAYER
        # =========================
        raw_response = call_model(prompt, req.n_predict or 100)

        # =========================
        # 5. SAFE RESPONSE PARSING
        # =========================
        if isinstance(raw_response, dict):
            reply = (
                raw_response.get("reply")
                or raw_response.get("response")
                or str(raw_response)
            )
        else:
            reply = str(raw_response)

        reply = (reply or "").strip()

        # =========================
        # 6. STORE ASSISTANT MESSAGE
        # =========================
        add_message(user_id, "assistant", reply)

        # =========================
        # 7. PERFORMANCE TRACKING
        # =========================
        latency = round(time.time() - start_time, 4)

        # =========================
        # 8. FINAL RESPONSE (CLEAN CONTRACT)
        # =========================
        return {
            "reply": reply,
            "intent": "GENERAL",
            "latency": latency
        }

    except Exception as e:
        # =========================
        # GLOBAL ERROR HANDLER
        # =========================
        print("[CHAT SERVICE ERROR]")
        print(traceback.format_exc())

        return {
            "reply": "Internal error occurred",
            "intent": "ERROR",
            "latency": round(time.time() - start_time, 4)
        }