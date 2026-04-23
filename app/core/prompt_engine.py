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
# 2. STRICT SYSTEM RULES (FIXED!)
# =========================
SYSTEM_RULES = """You are a helpful AI assistant. You MUST respond with exactly one JSON object in this exact format:

{"tool":"chat_reply","args":{"reply":"YOUR_REPLY_HERE"}}

CRITICAL RULES:
- Replace YOUR_REPLY_HERE with your actual response to the user
- Do NOT write "string" or any placeholder
- Do NOT add any text before or after the JSON
- Do NOT use markdown code blocks
- Do NOT add comments or explanations
- Respond in the same language as the user's message
- Keep replies natural and conversational"""


# =========================
# 3. MAIN PROMPT BUILDER (FIXED)
# =========================
def build_prompt(message: str, history: List[Dict]) -> str:
    history_block = _normalize_history(history)

    if history_block:
        prompt = f"""{SYSTEM_RULES}

Previous conversation:
{history_block}

User: {message}

Your response (JSON only):"""
    else:
        prompt = f"""{SYSTEM_RULES}

User: {message}

Your response (JSON only):"""

    return prompt
