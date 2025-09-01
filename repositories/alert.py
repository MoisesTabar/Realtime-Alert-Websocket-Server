from dataclasses import dataclass

from models.alert import Alert
from repositories.base import BaseRepository


@dataclass(slots=True)
class AlertRepository(BaseRepository[Alert]):
    maxlen: int = 10
