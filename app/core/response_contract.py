import json

def enforce_json(raw: str):
    """
    Final safety layer:
    Ensures ONLY valid JSON is returned.
    """

    if not raw:
        return None

    try:
        # محاولة مباشرة
        data = json.loads(raw)
        if isinstance(data, dict) and "reply" in data:
            return data["reply"]
    except:
        pass

    # إذا فشل → reject كامل
    return None