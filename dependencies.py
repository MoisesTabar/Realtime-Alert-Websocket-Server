from managers.connection_manager import ConnectionManager
from repositories.alert import AlertRepository
from repositories.chat import ChatRepository

# Module-level singletons shared across the app
manager = ConnectionManager()
alerts_repo = AlertRepository()
chats_repo = ChatRepository()


def get_alerts_repo() -> AlertRepository:
    return alerts_repo


def get_manager() -> ConnectionManager:
    return manager


def get_chats_repo() -> ChatRepository:
    return chats_repo
