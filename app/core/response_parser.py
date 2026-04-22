import json
import re

def parse_llm_response(raw: str):
    if not raw:
        return None

    # 🔥 خذ فقط أول JSON صحيح
    match = re.search(r"\{.*?\}", raw, re.DOTALL)
    if not match:
        return None

    try:
        data = json.loads(match.group(0))
        return data.get("reply")
    except:
        return None