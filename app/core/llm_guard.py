from app.core.response_parser import parse_llm_response
import time


def safe_call_llm(call_fn, max_retries=2):
    last_error = None

    for _ in range(max_retries):
        try:
            raw = call_fn()

            reply = parse_llm_response(raw)

            if reply:
                return reply

        except Exception as e:
            last_error = e
            time.sleep(0.2)

    return "Service temporarily unavailable"