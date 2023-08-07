from fastapi import APIRouter
router = APIRouter()

from . import chat

router.include_router(chat.router, prefix="/chat", tags=["聊天"])