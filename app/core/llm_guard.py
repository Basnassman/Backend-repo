from app.core.response_parser import parse_llm_response
import time

def safe_call_llm(call_fn, max_retries=2):
    for _ in range(max_retries):
        raw = call_fn()

        if isinstance(raw, dict):
            raw = raw.get("reply")

        print("RAW OUTPUT:", raw)

        reply = parse_llm_response(raw)

        if reply:
            return reply

    return "I couldn't generate a response."