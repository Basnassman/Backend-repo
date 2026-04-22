from app.core.prompt_engine import build_prompt
from app.core.model_router import call_model
from app.services.memory_service import add_message, get_history
from app.core.response_sanitizer import clean_output
from app.core.llm_guard import safe_call_llm
from app.core.text_cleaner import clean_text
from app.core.output_gate import extract_reply  # 🔥 ADD THIS
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

    reply = None

    try:
        # 1. store user message
        add_message(user_id, "user", message)

        # 2. load history
        history = get_history(user_id) or []

        # 3. build prompt
        prompt = build_prompt(message, history)

        # 4. model call wrapped in safe layer
        def call():
            return call_model(prompt, req.n_predict or 100)

        # 🔥 SAFE CALL
        
       
        reply = safe_call_llm(call)

        if isinstance(reply, dict):

         reply = reply.get("reply")

         reply = extract_reply(reply)

        if not reply:
         reply = "I couldn't generate a response."

    except Exception as e:
        print("[SAFE_CALL ERROR]", e)
        print(traceback.format_exc())
        reply = None

    # =========================
    # 5. FINAL OUTPUT PIPELINE (FIXED)
    # =========================
    reply = extract_reply(reply)

    if not reply:
        reply = "I couldn't generate a response."
    else:
        reply = str(reply).strip()
        reply = clean_output(reply)
        reply = clean_text(reply)

    # 6. store assistant reply
    add_message(user_id, "assistant", reply)

    # 7. latency
    latency = round(time.time() - start_time, 4)

    return {
        "reply": reply,
        "intent": "GENERAL",
        "latency": latency
    }