from controllers.alert import AlertController
from controllers.websocket import WebSocketController
from managers.connection_manager import ConnectionManager
from repositories.alert import AlertRepository
from repositories.chat import ChatRepository

# Module-level singletons shared across the app
manager = ConnectionManager()
alerts_repo = AlertRepository()
chats_repo = ChatRepository()

# Controllers
alert_controller = AlertController(manager, alerts_repo)
websocket_controller = WebSocketController(manager, chats_repo)

__all__ = [
    "manager",
    "alerts_repo",
    "chats_repo",
    "get_alert_controller",
    "get_websocket_controller",
]


def get_alert_controller() -> AlertController:
    return alert_controller


def get_websocket_controller() -> WebSocketController:
    return websocket_controller
