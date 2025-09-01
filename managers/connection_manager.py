import asyncio
import logging
from dataclasses import dataclass, field

from fastapi import WebSocket
from starlette.websockets import WebSocketState


@dataclass(slots=True)
class ConnectionManager:
    """
    Manages active WebSocket connections and handles broadcasting.
    """

    active_connections: set[WebSocket] = field(default_factory=set)
    _locks: dict[WebSocket, asyncio.Lock] = field(default_factory=dict, repr=False)

    def _is_connected(self, socket: WebSocket) -> bool:
        """Return True if both app and client states are CONNECTED."""
        app_state = getattr(socket, "application_state", None)
        client_state = getattr(socket, "client_state", None)
        return (
            app_state == WebSocketState.CONNECTED
            and client_state == WebSocketState.CONNECTED
        )

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.add(websocket)
        self._locks[websocket] = asyncio.Lock()
        logging.info(
            f"[manager={id(self)}] Connected; total={len(self.active_connections)}"
        )

    def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.discard(websocket)
        self._locks.pop(websocket, None)
        logging.info(
            f"[manager={id(self)}] Disconnected; total={len(self.active_connections)}"
        )

    async def broadcast_json(self, data: dict) -> None:
        connections = list(self.active_connections)
        logging.debug(f"[manager={id(self)}] Broadcasting to {len(connections)} conns")
        for socket in connections:
            # Skip sockets that are no longer connected
            if not self._is_connected(socket):
                logging.debug(f"[manager={id(self)}] Skipping closed socket")
                self.disconnect(socket)
                continue
            lock = self._locks.get(socket)
            if lock is None:
                # Socket might have been added without lock due to race;
                lock = asyncio.Lock()
                self._locks[socket] = lock
            try:
                async with lock:
                    # Re-check state inside the lock right before sending
                    if not self._is_connected(socket):
                        logging.debug(f"[manager={id(self)}] Closed before send")
                        raise RuntimeError("WebSocket not connected at send time")
                    await socket.send_json(data)
            except Exception:
                logging.exception(f"[manager={id(self)}] Send failed; removing socket")
                self.disconnect(socket)
