from app.core.prompt_engine import build_prompt
from app.core.model_router import call_model
from app.services.memory_service import add_message, get_history
import time
import traceback


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
        # 1. store user message
        add_message(user_id, "user", message)

        # 2. load history
        history = get_history(user_id) or []

        # 3. build prompt
        prompt = build_prompt(message, history)

        # 4. call model
        raw_response = call_model(prompt, req.n_predict or 100)

        # 5. safe parsing
        if isinstance(raw_response, dict):
            reply = (
                raw_response.get("reply")
                or raw_response.get("response")
                or raw_response.get("content")
                or raw_response.get("text")
            )
        else:
            reply = str(raw_response)

        reply = (reply or "").strip()

        if not reply:
            reply = "I couldn't generate a response. Please try again."

        # 6. store assistant reply
        add_message(user_id, "assistant", reply)

        # 7. latency
        latency = round(time.time() - start_time, 4)

        return {
            "reply": reply,
            "intent": "GENERAL",
            "latency": latency
        }

    except Exception:
        print(traceback.format_exc())

        return {
            "reply": "Internal error occurred",
            "intent": "ERROR",
            "latency": round(time.time() - start_time, 4)
        }