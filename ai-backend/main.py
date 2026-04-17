from fastapi import FastAPI
from pydantic import BaseModel
from services.ai_engine import generate_response

app = FastAPI()


class ChatRequest(BaseModel):
    message: str | None = None
    prompt: str | None = None
    n_predict: int | None = 100


def extract_message(req: ChatRequest):
    return req.message or req.prompt or ""


@app.post("/chat")
def chat(req: ChatRequest):

    message = extract_message(req)

    return generate_response(message, req.n_predict or 100)