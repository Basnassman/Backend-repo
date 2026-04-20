from fastapi import APIRouter
from api.schemas.chat_schema import ChatRequest
from services.chat_service import handle_chat

router = APIRouter()

@router.post("/chat")
def chat(req: ChatRequest):
    return handle_chat(req)