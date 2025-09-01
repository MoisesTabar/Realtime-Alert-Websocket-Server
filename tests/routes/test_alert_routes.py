from fastapi import FastAPI
from fastapi.testclient import TestClient

from routes import alert as alert_module
from routes.alert import router as alert_router


class FakeAlertController:
    def __init__(self):
        self.history = []
        self.posted = []

    def get_history(self):
        return self.history

    async def post_alert(self, alert):
        self.posted.append(alert)
        return alert


def create_app_with_overrides(controller):
    app = FastAPI()
    app.include_router(alert_router)

    app.dependency_overrides[alert_module.get_alert_controller] = lambda: controller
    return app


def test_get_alert_history_returns_list():
    controller = FakeAlertController()
    controller.history = []
    app = create_app_with_overrides(controller)
    client = TestClient(app)

    r = client.get("/alerts/history")
    assert r.status_code == 200
    assert r.json() == []


def test_post_alert_roundtrips_and_calls_controller():
    controller = FakeAlertController()
    app = create_app_with_overrides(controller)
    client = TestClient(app)

    payload = {
        "message": "m",
        "location": "L",
        "timestamp": "2024-01-01T00:00:00Z",
    }
    r = client.post("/alerts/", json=payload)
    assert r.status_code == 200

    body = r.json()
    # id auto-generated
    assert isinstance(body.get("id"), str) and body["id"]
    assert body["message"] == "m"
    assert body["location"] == "L"
    assert body["timestamp"].startswith("2024-01-01T00:00:00")

    # controller received the same alert object
    assert len(controller.posted) == 1
