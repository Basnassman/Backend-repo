from typing import List, Dict


# =========================
# 1. MEMORY NORMALIZER (cleaner)
# =========================
def _normalize_history(history: List[Dict], limit: int = 5) -> str:
    output = []

    for msg in history[-limit:]:
        role = msg.get("role")
        content = (msg.get("content") or "").strip()

        if not content:
            continue

        # 🔥 تبسيط بدون رموز قد تربك النموذج
        if role == "user":
            output.append(f"User: {content}")
        elif role == "assistant":
            output.append(f"Assistant: {content}")

    return "\n".join(output)


# =========================
# 2. STRICT SYSTEM RULES (SIMPLIFIED - IMPORTANT)
# =========================
SYSTEM_RULES = """
You are a strict API engine.

Return ONLY valid JSON.

Rules:
- Only JSON output allowed
- No explanations
- No markdown
- No SYSTEM / CONTEXT / INPUT tags
- No extra text before or after JSON

Format:
{"reply":"string"}

If unsure:
{"reply":""}
""".strip()


# =========================
# 3. INTENT FILTER (simplified)
# =========================
def _detect_mode(message: str) -> str:
    msg = message.lower()

    if any(k in msg for k in ["code", "python", "dart", "flutter"]):
        return "CODE"

    if any(k in msg for k in ["what", "how", "why", "اشرح", "لماذا"]):
        return "EXPLAIN"

    if any(k in msg for k in ["hi", "hello", "السلام", "مرحبا"]):
        return "CHAT"

    return "GENERAL"


# =========================
# 4. MAIN PROMPT BUILDER (SIMPLIFIED + STRONGER)
# =========================
def build_prompt(message: str, history: List[Dict]) -> str:
    history_block = _normalize_history(history)

    prompt = f"""
{SYSTEM_RULES}

Conversation:
{history_block if history_block else "No history"}

User message:
{message}

IMPORTANT:
Respond ONLY with JSON:
{{"reply":"..."}}
""".strip()

    return prompt