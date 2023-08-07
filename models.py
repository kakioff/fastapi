from fastapi import WebSocket
from pydantic import BaseModel
from typing import List, Dict
class SendData(BaseModel):
    succ: bool = True
    err_msg: str = ""
    data: dict = {}

class WebSocketConnectionManager:
    def __init__(self, name:str=""):
        self.active_connections: dict[str, WebSocket] = {}
        self.name=name

    async def connect(self, websocket: WebSocket, token: str):
        await websocket.accept()
        self.active_connections[token] = websocket

    def disconnect(self, token: str, websocket: WebSocket | None = None):
        try:
            del self.active_connections[token]
        except:
            print(f"{token} is not in list")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for token, connection in self.active_connections.items():
            await connection.send_text(message)