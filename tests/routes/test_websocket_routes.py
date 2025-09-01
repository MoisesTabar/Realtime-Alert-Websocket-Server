from fastapi import FastAPI
from fastapi.testclient import TestClient

from routes.websocket import router as ws_router


class FakeWSController:
    def __init__(self):
        self.connected = []
        self.disconnected = []
        self.handled = []

    async def connect(self, websocket):
        self.connected.append(websocket)
        await websocket.accept()

    def disconnect(self, websocket):
        self.disconnected.append(websocket)

    async def handle_json(self, data: dict):
        self.handled.append(data)


def create_app_with_overrides(controller):
    app = FastAPI()
    app.include_router(ws_router)

    from routes import websocket as ws_module

    app.dependency_overrides[ws_module.get_websocket_controller] = lambda: controller
    return app


def test_websocket_endpoint_connect_handle_disconnect_flow():
    controller = FakeWSController()
    app = create_app_with_overrides(controller)
    client = TestClient(app)

    with client.websocket_connect("/ws") as ws:
        ws.send_json({"sender": "s", "message": "hello"})
    # Exiting context manager triggers disconnect via close -> WebSocketDisconnect

    # Assert controller methods were called appropriately
    assert len(controller.connected) == 1
    assert controller.handled == [{"sender": "s", "message": "hello"}]
    assert len(controller.disconnected) == 1
