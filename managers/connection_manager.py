from dataclasses import dataclass, field

from fastapi import WebSocket


@dataclass(slots=True)
class ConnectionManager:
    """
    Manages active WebSocket connections and handles broadcasting.
    """

    active_connections: set[WebSocket] = field(default_factory=set)

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.discard(websocket)

    async def broadcast_json(self, data: dict) -> None:
        connections = list(self.active_connections)
        for socket in connections:
            try:
                await socket.send_json(data)
            except Exception:
                self.disconnect(socket)
