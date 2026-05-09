from fastapi import APIRouter

from schemas.api import ChatRequest, ChatResponse
from services.openai_service import openai_chat_service


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def chat(payload: ChatRequest):
    return ChatResponse(reply=openai_chat_service.chat(payload.user_id, payload.message))
