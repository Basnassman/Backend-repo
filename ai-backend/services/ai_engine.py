import requests
from services.memory import add_message, get_history

LLAMA_API_URL = "http://54.227.171.175:3000/chat"
API_KEY = "712825736aA$"


def detect_intent(text: str):
    text = text.lower()

    if any(k in text for k in ["error", "bug", "exception", "fail", "خطأ", "مشكلة"]):
        return "DEBUG"

    if any(k in text for k in ["fix", "solve", "implement", "حل", "code"]):
        return "SOLVE"

    if any(k in text for k in ["explain", "what", "كيف", "اشرح", "learn"]):
        return "TEACH"

    return "GENERAL"


def build_prompt(message: str, history: list, intent: str):

    system = f"""
You are a highly skilled programming assistant.

Rules:
- Respond in the same language as the user
- Be clear and concise
- Do not repeat the user message
- Output only the final answer
"""

    persona = {
        "DEBUG": "You are a senior software engineer specialized in debugging.",
        "SOLVE": "You solve coding problems step-by-step.",
        "TEACH": "You are a programming teacher who explains simply.",
        "GENERAL": "You are a helpful assistant."
    }.get(intent, "You are a helpful assistant.")

    formatted_history = "\n".join(
        [f"{m['role']}: {m['content']}" for m in history]
    )

    return f"""
{system}

{persona}

Conversation:
{formatted_history}

User: {message}
Assistant:
""".strip()


def call_llama(prompt: str, n_predict: int):

    try:
        response = requests.post(
            LLAMA_API_URL,
            json={
                "prompt": prompt,
                "n_predict": n_predict,
                "temperature": 0.3,
                "stop": ["User:", "Assistant:"]
            },
            headers={"x-api-key": API_KEY},
            timeout=30
        )

        return response.json()

    except Exception as e:
        return {"reply": str(e)}


def generate_response(message: str, n_predict: int, user_id: str):

    add_message(user_id, "user", message)

    intent = detect_intent(message)
    history = get_history(user_id)

    prompt = build_prompt(message, history, intent)

    result = call_llama(prompt, n_predict)

    reply = (
        result.get("reply")
        or result.get("response")
        or result.get("content")
        or str(result)
    )

    add_message(user_id, "assistant", reply)

    return {
        "intent": intent,
        "reply": reply
    }