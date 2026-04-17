from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

# ====== CONFIG ======
LLAMA_API_URL = "http://54.227.171.175:3000/chat"

# 🔐 API KEY (لازم يطابق Node.js)
API_KEY = "712825736aA$"

class ChatRequest(BaseModel):
    message: str


# ====== INTENT ======
def detect_intent(text: str):
    text = text.lower()

    if "error" in text or "bug" in text or "خطأ" in text:
        return "DEBUG"

    if "solve" in text or "حل" in text:
        return "SOLVE"

    if "explain" in text or "اشرح" in text:
        return "TEACH"

    return "GENERAL"


# ====== PROMPT ======
def build_prompt(message: str, intent: str):

    instruction = {
        "TEACH": "Explain clearly step by step with simple examples.",
        "SOLVE": "Give the solution first then short explanation.",
        "DEBUG": "Find the issue and explain the fix clearly.",
        "GENERAL": "Answer clearly and simply."
    }

    return f"""
You are a helpful programming tutor.

Instruction:
{instruction[intent]}

Question:
{message}

Answer only. Do not repeat the question.
""".strip()


# ====== CALL NODE.JS (WITH AUTH) ======
def call_llama(prompt: str):

    headers = {
        "x-api-key": API_KEY   # 🔐 هذا هو المفتاح الصحيح
    }

    response = requests.post(
        LLAMA_API_URL,
        json={
            "prompt": prompt,
            "temperature": 0.5,
            "max_tokens": 400
        },
        headers=headers
    )

    return response.json()


# ====== API ======
@app.post("/chat")
def chat(req: ChatRequest):

    intent = detect_intent(req.message)
    prompt = build_prompt(req.message, intent)

    llama_response = call_llama(prompt)

    # تنظيف الرد بأمان
    result = (
        llama_response.get("reply")
        or llama_response.get("content")
        or llama_response.get("response")
        or str(llama_response)
    )

    return {
        "intent": intent,
        "response": result
    }