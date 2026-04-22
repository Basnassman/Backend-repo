import re
import json

def extract_reply(raw: str):
    if not raw:
        return None

    # 1. حاول استخراج JSON من أي نص
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if not match:
        return None

    try:
        data = json.loads(match.group(0))

        if isinstance(data, dict):
            return data.get("reply")

    except:
        pass

    return None