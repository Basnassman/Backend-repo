from typing import List, Dict


# =========================
# 1. MEMORY NORMALIZER
# =========================
def _normalize_history(history: List[Dict], limit: int = 6) -> str:
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
# 2. STRICT SYSTEM RULES (IMPROVED)
# =========================
SYSTEM_RULES = """
You are a STRICT JSON API engine.

ABSOLUTE RULES:
- Output ONLY valid JSON
- NEVER include <SYSTEM>, <CONTEXT>, <INPUT>, <OUTPUT>
- NEVER repeat the prompt
- NEVER include explanations
- NEVER include markdown or text outside JSON
- If you fail, output {"reply": ""}

HARD FORMAT:
{"reply":"string"}
""".strip()


# =========================
# 3. INTENT FILTER
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
# 4. MAIN PROMPT BUILDER
# =========================
def build_prompt(message: str, history: List[Dict]) -> str:
    mode = _detect_mode(message)
    history_block = _normalize_history(history)

    mode_rules = {
        "CODE": "Return ONLY code inside JSON.\n",
        "EXPLAIN": "Be short and factual.\n",
        "CHAT": "Be natural but very short.\n",
        "GENERAL": "Be direct and minimal.\n",
    }

    prompt = f"""
SYSTEM:
{SYSTEM_RULES}

MODE RULE:
{mode_rules.get(mode)}

IMPORTANT:
Return ONLY this JSON:
{{"reply":"..." }}

CONTEXT:
{history_block if history_block else "EMPTY"}

USER:
{message}

RESPONSE (JSON ONLY):
""".strip()

    return prompt