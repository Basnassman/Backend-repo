from app.core.prompt_engine import build_prompt
from app.core.model_router import call_model
from app.services.memory_service import add_message, get_history
from app.core.llm_guard import safe_call_llm
from app.core.response_parser import parse_tool_response
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
        # 1. حفظ رسالة المستخدم
        add_message(user_id, "user", message)

        # 2. جلب التاريخ
        history = get_history(user_id) or []

        # 3. بناء prompt
        prompt = build_prompt(message, history)

        # 4. استدعاء النموذج
        def call():
            return call_model(prompt, req.n_predict or 100)

        raw_reply = safe_call_llm(call)

        # 5. معالجة + استخراج + تنظيف داخل parser
        reply = parse_tool_response(raw_reply)

        # 6. fallback
        if not reply:
            reply = "I couldn't generate a response."

        # 7. حفظ الرد
        add_message(user_id, "assistant", reply)

        # 8. latency
        latency = round(time.time() - start_time, 4)

        return {
            "reply": reply,
            "intent": "GENERAL",
            "latency": latency
        }

    except Exception as e:
        print("[CHAT ERROR]", e)
        print(traceback.format_exc())

        latency = round(time.time() - start_time, 4)

        return {
            "reply": "Internal error occurred",
            "intent": "ERROR",
            "latency": latency
        }