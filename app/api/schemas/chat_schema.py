from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = "default"
    n_predict: Optional[int] = 100


class ChatResponse(BaseModel):
    reply: str
    intent: str