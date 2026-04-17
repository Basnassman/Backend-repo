from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

# ====== CONFIG ======
LLAMA_API_URL = "http://54.227.171.175:3000/chat"

# ====== REQUEST MODEL ======
class ChatRequest(BaseModel):
    message: str

# ====== INTENT DETECTION ======
def detect_intent(text: str):
    text = text.lower()

    if any(word in text for word in ["اشرح", "explain", "what is"]):
        return "TEACH"

    if any(word in text for word in ["حل", "solve", "code"]):
        return "SOLVE"

    if any(word in text for word in ["error", "bug", "خطأ"]):
        return "DEBUG"

    return "GENERAL"

# ====== PROMPT ENGINE ======
def build_prompt(message: str, intent: str):
    base = """
You are an expert programming tutor.
You explain programming clearly and adapt to user level.
"""

    styles = {
        "TEACH": "Explain step by step with examples.",
        "SOLVE": "Give full working solution first then short explanation.",
        "DEBUG": "Find bug first then explain and fix it.",
        "GENERAL": "Give balanced clear answer."
    }

    return f"""
{base}

Mode: {styles[intent]}

User Question:
{message}

Answer clearly and structured.
"""

# ====== CALL LLAMA ======
def call_llama(prompt: str):
    response = requests.post(
        LLAMA_API_URL,
        json={
            "prompt": prompt,
            "temperature": 0.7,
            "max_tokens": 512
        }
    )
    return response.json()

# ====== API ENDPOINT ======
@app.post("/chat")
def chat(req: ChatRequest):

    intent = detect_intent(req.message)
    prompt = build_prompt(req.message, intent)

    llama_response = call_llama(prompt)

    return {
        "intent": intent,
        "response": llama_response.get("content", llama_response)
    }