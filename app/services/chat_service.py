from app.core.prompt_engine import build_prompt
from app.core.model_router import call_model
from app.services.memory_service import add_message, get_history
from app.core.response_sanitizer import clean_output
from app.core.llm_guard import safe_call_llm
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

        # 4. model call wrapped in safe layer
        def call():
         result = call_model(prompt, req.n_predict or 100)

        # دعم كل أنواع الردود
         if isinstance(result, dict):
          return result.get("reply") or result.get("response") or str(result)

         return str(result)

         reply = safe_call_llm(call)


        # 5. cleanup
        reply = (reply or "").strip()
        reply = clean_output(reply)

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

        latency = round(time.time() - start_time, 4)

        return {
            "reply": "Internal error occurred",
            "intent": "ERROR",
            "latency": latency
        }