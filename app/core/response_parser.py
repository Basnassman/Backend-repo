import json

def parse_llm_response(raw: str):
    try:
        data = json.loads(raw)

        if isinstance(data, dict) and "reply" in data:
            return data["reply"]

        return None

    except Exception:
        return None