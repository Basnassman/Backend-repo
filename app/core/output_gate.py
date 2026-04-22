import json
import re

def extract_reply(raw: str):
    if not raw:
        return None

    raw = str(raw)

    # 🔥 إزالة التعليقات (# ...)
    raw = re.sub(r"#.*", "", raw)

    # 🔥 إزالة code blocks
    raw = re.sub(r"```.*?```", "", raw, flags=re.DOTALL)

    # 🔥 استخراج أول JSON فقط
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        return None

    try:
        data = json.loads(match.group(0))
        return data.get("reply")
    except:
        return None