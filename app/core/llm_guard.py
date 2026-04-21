from app.core.response_parser import parse_llm_response
import time

def safe_call_llm(call_fn, max_retries=2):
    last = None

    for _ in range(max_retries):
        raw = call_fn()

        print("RAW OUTPUT:", raw)

        reply = parse_llm_response(raw)

        if reply:
            return reply

        last = raw
        time.sleep(0.3)

    return "Service temporarily unavailable"