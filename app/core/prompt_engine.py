def build_prompt(message: str, history: list) -> str:

    system_rules = """
You are a highly reliable AI assistant.

STRICT RULES:
- Respond ONLY in the user's language
- Be concise and direct
- Do NOT simulate conversation
- Do NOT write "User:" or "Assistant:"
- Do NOT add explanations unless asked
- Output ONLY the final answer
"""

    formatted_history = "\n---\n".join(
        [f"USER:\n{m['content']}" if m["role"] == "user"
         else f"ASSISTANT:\n{m['content']}" for m in history]
    )

    prompt = f"""
{system_rules}

CONVERSATION:
{formatted_history}

USER:
{message}

ASSISTANT:
""".strip()

    return prompt