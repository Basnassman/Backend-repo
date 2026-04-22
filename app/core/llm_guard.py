from app.core.response_parser import parse_llm_response
import time

def safe_call_llm(call_fn, max_retries=2):
    for _ in range(max_retries):
        raw = call_fn()

        print("RAW OUTPUT:", raw)

        if raw and isinstance(raw, str) and raw.strip():
            return raw.strip()

    return "I couldn't generate a response."