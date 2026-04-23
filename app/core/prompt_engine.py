from typing import List, Dict


# =========================
# 1. MEMORY NORMALIZER (SAFE)
# =========================
def _normalize_history(history: List[Dict], limit: int = 3) -> str:
    output = []

    for msg in history[-limit:]:
        role = msg.get("role")
        content = (msg.get("content") or "").strip()

        if not content:
            continue

        if role == "user":
            output.append(f"User: {content}")
        elif role == "assistant":
            output.append(f"Assistant: {content}")

    return "\n".join(output)


# =========================
# 2. STRICT SYSTEM RULES (CLEAN)
# =========================
SYSTEM_RULES = """
You are a strict JSON API.

Return ONLY one JSON object.

Do not continue the conversation.
Do not simulate multiple turns.
Do not add comments.
Do not add explanations.

Format:
{"reply":"..."}

If you add anything else, the output is invalid.
"""


# =========================
# 3. MAIN PROMPT BUILDER (FIXED)
# =========================
def build_prompt(message: str, history: List[Dict]) -> str:
    # 🔥 مهم: نحد من تأثير history
    history_block = _normalize_history(history)

    if history_block:
        prompt = f"""
{SYSTEM_RULES}

Conversation:
{history_block}

User:
{message}
""".strip()
    else:
        prompt = f"""
{SYSTEM_RULES}

User:
{message}
""".strip()

    return prompt