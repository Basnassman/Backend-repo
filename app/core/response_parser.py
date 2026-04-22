import json
import re

def parse_llm_response(raw: str):
    if not raw:
        return None

    # 🔥 استخراج كل JSONs
    matches = re.findall(r"\{[^{}]*\}", raw)

    for m in matches:
        try:
            data = json.loads(m)
            if isinstance(data, dict) and "reply" in data:
                return data["reply"]
        except:
            continue

    return None