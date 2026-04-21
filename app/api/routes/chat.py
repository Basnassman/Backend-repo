from fastapi import APIRouter, HTTPException, Request
from api.schemas.chat_schema import ChatRequest
from app.services.chat_service import handle_chat
import time

router = APIRouter()


# =========================
# SIMPLE REQUEST LOGGING  
# =========================
def _log_request(req: ChatRequest):
    print(f"[CHAT REQUEST] message={req.message}")


# =========================
# POST /chat
# =========================
@router.post("/chat")
async def chat(req: ChatRequest, request: Request):
    start_time = time.time()

    try:
        # 1. basic validation guard
        if not req.message:
            raise HTTPException(
                status_code=400,
                detail="message is required"
            )

        # 2. log request (production debugging)
        _log_request(req)

        # 3. business logic layer
        response = handle_chat(req)

        # 4. performance tracking
        duration = round(time.time() - start_time, 4)

        return {
            "success": True,
            "response": response,
            "latency": duration
        }

    except HTTPException as he:
        raise he

    except Exception as e:
        # global fallback error (like production APIs)
        print(f"[CHAT ERROR] {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )