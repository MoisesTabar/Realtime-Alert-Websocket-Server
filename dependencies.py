from managers.connection_manager import ConnectionManager
from repositories.alert import AlertRepository
from repositories.chat import ChatRepository


def get_alerts_repo() -> AlertRepository:
    return AlertRepository()


def get_manager() -> ConnectionManager:
    return ConnectionManager()


def get_chats_repo() -> ChatRepository:
    return ChatRepository()
