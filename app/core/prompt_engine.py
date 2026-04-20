from typing import List, Dict


# =========================
# 1. MEMORY NORMALIZER
# =========================
def _normalize_history(history: List[Dict], limit: int = 6) -> str:
    """
    Converts chat history into stable structured format
    """
    output = []

    for msg in history[-limit:]:
        role = msg.get("role")
        content = (msg.get("content") or "").strip()

        if not content:
            continue

        if role == "user":
            output.append(f"[U] {content}")
        elif role == "assistant":
            output.append(f"[A] {content}")

    return "\n".join(output)


# =========================
# 2. PROMPT GUARD (CORE RULES)
# =========================
SYSTEM_PROMPT = (
    "You are a controlled AI execution engine.\n"
    "You are NOT a chatbot.\n\n"
    "HARD RULES:\n"
    "- Output ONLY final answer\n"
    "- No explanations\n"
    "- No repetition\n"
    "- No meta text (no Note, no Correct response)\n"
    "- No role labels in output\n"
    "- If input is greeting → respond with minimal greeting only\n"
    "- If input is code request → output only code\n"
    "- Always stay deterministic and minimal\n"
)


# =========================
# 3. INTENT FILTER (light routing)
# =========================
def _detect_mode(message: str) -> str:
    msg = message.lower()

    if any(k in msg for k in ["code", "python", "dart", "flutter"]):
        return "CODE"

    if any(k in msg for k in ["what", "how", "اشرح", "لماذا"]):
        return "EXPLAIN"

    if any(k in msg for k in ["hi", "hello", "السلام", "مرحبا"]):
        return "CHAT"

    return "GENERAL"


# =========================
# 4. MAIN PROMPT BUILDER
# =========================
def build_prompt(message: str, history: List[Dict]) -> str:
    mode = _detect_mode(message)
    history_block = _normalize_history(history)

    mode_rules = {
        "CODE": "- Return ONLY code, no explanation\n",
        "EXPLAIN": "- Be short, minimal explanation allowed\n",
        "CHAT": "- Respond naturally but very short\n",
        "GENERAL": "- Be direct and minimal\n",
    }

    prompt = f"""
<SYSTEM>
{SYSTEM_PROMPT}
{mode_rules.get(mode)}
</SYSTEM>

<CONTEXT>
{history_block if history_block else "EMPTY"}
</CONTEXT>

<INPUT>
{message}
</INPUT>

<OUTPUT>
""".strip()

    return prompt