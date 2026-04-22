import json
import re


def extract_json(text: str):
    """
    Extract first valid JSON object from raw LLM output
    """
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if not match:
        return None

    try:
        return json.loads(match.group())
    except:
        return None


def clean_reply(text: str) -> str:
    """
    Minimal safe cleaning only (NOT aggressive)
    """
    if not text:
        return ""

    return (
        text.strip()
        .replace("\n", " ")
        .replace("\t", " ")
    )


def parse_llm_response(raw: str) -> str:
    """
    Main pipeline:
    RAW LLM OUTPUT → JSON → reply string
    """

    if not raw:
        return None

    # 1. try direct JSON (ideal case)
    try:
        data = json.loads(raw)
        if isinstance(data, dict) and "reply" in data:
            return clean_reply(str(data["reply"]))
    except:
        pass

    # 2. try extract JSON from messy output
    data = extract_json(raw)
    if data and "reply" in data:
        return clean_reply(str(data["reply"]))

    # 3. fallback: treat as plain text
    return clean_reply(raw)