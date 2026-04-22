from app.core.response_contract import enforce_json

def safe_call_llm(call_fn, max_retries=2):
    for _ in range(max_retries):
        raw = call_fn()

        reply = enforce_json(raw)

        if reply:
            return reply

    return "Service temporarily unavailable"