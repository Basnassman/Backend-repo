import json
import re

def extract_reply(raw):
    if not raw:
        return None

    raw = str(raw)

    # 🔥 احذف كل شيء قبل أول {
    start = raw.find("{")
    end = raw.rfind("}")

    if start == -1 or end == -1:
        return None

    json_str = raw[start:end+1]

    try:
        return json.loads(json_str).get("reply")
    except:
        return None