import json
import re

def parse_llm_response(raw: str):
    if not raw:
        return None

    try:
        # 1. حاول استخراج أول JSON صحيح فقط
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            return None

        json_str = match.group(0)

        data = json.loads(json_str)

        if isinstance(data, dict):
            return data.get("reply")

        return None

    except Exception:
        return None