from dataclasses import dataclass

from fastapi import WebSocket

from managers.connection_manager import ConnectionManager
from models.message import ChatMessage
from repositories.chat import ChatRepository


@dataclass(slots=True)
class WebSocketController:
    manager: ConnectionManager
    repository: ChatRepository

    async def connect(self, websocket: WebSocket) -> None:
        await self.manager.connect(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self.manager.disconnect(websocket)

    async def handle_json(self, data: dict) -> None:
        message = ChatMessage(**data)
        self.repository.add(message)
        await self.manager.broadcast_json({"type": "message", **message.model_dump()})
