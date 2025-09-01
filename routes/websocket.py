from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from controllers.websocket import WebSocketController
from dependencies import get_websocket_controller

router = APIRouter(tags=["websocket"])


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    controller: WebSocketController = Depends(get_websocket_controller),
):
    await controller.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await controller.handle_json(data)
    except WebSocketDisconnect:
        controller.disconnect(websocket)
    except Exception:
        controller.disconnect(websocket)
