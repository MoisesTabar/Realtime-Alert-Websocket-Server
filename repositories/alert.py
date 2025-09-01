from collections import deque
from dataclasses import dataclass, field

from models.alert import Alert


@dataclass(slots=True)
class AlertRepository:
    """
    In-memory store for alerts with fixed max length.
    """

    maxlen: int = 10
    _alerts: deque = field(default_factory=lambda: deque(maxlen=10))

    def add(self, alert: Alert) -> None:
        self._alerts.appendleft(alert)

    def get_all(self) -> list[Alert]:
        return list(self._alerts)
