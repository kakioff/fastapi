from . import router
from fastapi import Query

@router.get("/gpt/history")
def history(chat_id=Query()):
    return chat_id
