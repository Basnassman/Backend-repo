import json
import re


# =========================
# 1. EXTRACT JSON (SAFE)
# =========================
def extract_json(text: str):
    """
    Extract first valid JSON object from raw LLM output
    """
    if not text:
        return None

    # 🔥 أخذ أول JSON فقط (non-greedy)
    match = re.search(r'\{.*?\}', text, re.DOTALL)
    if not match:
        return None

    try:
        return json.loads(match.group())
    except:
        return None


# =========================
# 2. CLEAN OUTPUT
# =========================
def clean_reply(text: str) -> str:
    """
    Minimal safe cleaning only
    """
    if not text:
        return ""

    text = str(text)

    # 🔥 قص أي ضوضاء من LLM
    text = text.split("//")[0]
    text = text.split("User:")[0]
    text = text.split("Assistant:")[0]

    return (
        text.strip()
        .replace("\n", " ")
        .replace("\t", " ")
    )


# =========================
# 3. MAIN PARSER PIPELINE
# =========================
def parse_llm_response(raw: str) -> str:
    """
    RAW → JSON → reply
    """

    if not raw:
        return None

    # 1. محاولة JSON مباشر
    try:
        data = json.loads(raw)
        if isinstance(data, dict) and "reply" in data:
            return clean_reply(data["reply"])
    except:
        pass

    # 2. استخراج JSON من نص ملخبط
    data = extract_json(raw)
    if data and isinstance(data, dict) and "reply" in data:
        return clean_reply(data["reply"])

    # 3. fallback (نص عادي)
    return clean_reply(raw)