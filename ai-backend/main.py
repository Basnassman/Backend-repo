from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # مهم
    allow_credentials=False,  # 🔥 غيرها إلى False
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    text: str

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/chat")
def chat(msg: Message):
    return {"reply": f"🤖 AI Response: {msg.text}"}