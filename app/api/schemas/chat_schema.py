from pydantic import BaseModel, Field
from typing import Optional


# =========================
# REQUEST SCHEMA
# =========================
class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        description="User input message"
    )

    user_id: Optional[str] = Field(
        default="default",
        max_length=100
    )

    n_predict: Optional[int] = Field(
        default=100,
        ge=1,     # >= 1
        le=1000   # <= 1000
    )


# =========================
# RESPONSE SCHEMA
# =========================
class ChatResponse(BaseModel):
    reply: str = Field(
        ...,
        description="Model generated response"
    )

    intent: Optional[str] = Field(
        default="GENERAL"
    )

    # 🔥 مهم جداً في production (debugging + observability)
    latency: Optional[float] = None

    # 🔥 future-proofing (for multi-model systems)
    model: Optional[str] = None