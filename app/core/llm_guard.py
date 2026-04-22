from app.core.response_parser import parse_llm_response
import time

def safe_call_llm(call_fn, max_retries=2):
    last = None

    for _ in range(max_retries):
        raw = call_fn()

        print("RAW OUTPUT:", raw)

        try:
            reply = parse_llm_response(raw)
        except Exception as e:
            print("PARSE ERROR:", e)
            reply = None

        # fallback آمن
        if reply:
            return reply

        # إذا parser فشل → رجّع raw بدل ما تضيع
        if isinstance(raw, str) and raw.strip():
            return raw.strip()

        last = raw
        time.sleep(0.3)

    return "I couldn't process the response."