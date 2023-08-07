import json
from main import app as ws
from fastapi import Header, WebSocket, WebSocketDisconnect

class IndexModel:
    ip: str
    ua: str


from models import WebSocketConnectionManager
manager = WebSocketConnectionManager("base")

@ws.get("/ws")
def ws_list():
    all_usrs = manager.active_connections
    user_list = []
    for token in all_usrs:
        user_list.append({
            "user": token
        })
    return {'name':manager.name, 'users':user_list}
# websocket
@ws.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token=Header(default="**")):
    await manager.connect(websocket, token)
    try:
        await manager.send_personal_message("connected", websocket)
        while True:
            data = await websocket.receive_json()
            await manager.broadcast(f"Client #{token} says: {json.dumps(data)}")
    except WebSocketDisconnect:
        manager.disconnect(token)
        await manager.broadcast(f"Client #{token} left the chat")
