from managers.connection_manager import ConnectionManager
from repositories.alert import AlertRepository


def get_alerts_repo() -> AlertRepository:
    return AlertRepository()


def get_manager() -> ConnectionManager:
    return ConnectionManager()
