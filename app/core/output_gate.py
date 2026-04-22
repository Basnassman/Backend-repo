import json
import re

def extract_reply(raw: str):
    if not raw:
        return None

    # 🔥 حذف الكود أولاً
    cleaned = re.sub(r"```.*?```", "", raw, flags=re.DOTALL)

    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if not match:
        return None

    try:
        data = json.loads(match.group(0))
        return data.get("reply")
    except:
        return None