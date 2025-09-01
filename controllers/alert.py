from dataclasses import dataclass

from managers.connection_manager import ConnectionManager
from models.alert import Alert
from repositories.alert import AlertRepository


@dataclass(slots=True)
class AlertController:
    manager: ConnectionManager
    repository: AlertRepository

    def get_history(self) -> list[Alert]:
        return self.repository.get_all()

    async def post_alert(self, alert: Alert) -> Alert:
        self.repository.add(alert)
        await self.manager.broadcast_json({"type": "alert", **alert.model_dump()})
        return alert
