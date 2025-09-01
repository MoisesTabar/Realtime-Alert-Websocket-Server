from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from dependencies import get_chats_repo, get_manager
from managers.connection_manager import ConnectionManager
from models.message import ChatMessage
from repositories.base import BaseRepository

router = APIRouter(tags=["websocket"])


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    manager: ConnectionManager = Depends(get_manager),
    repository: BaseRepository = Depends(get_chats_repo),
):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            message = ChatMessage(**data)
            repository.add(message)
            await manager.broadcast_json({"type": "message", **message.model_dump()})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)
