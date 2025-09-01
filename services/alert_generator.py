import asyncio
from datetime import datetime, timezone
from itertools import count, cycle

from managers.connection_manager import ConnectionManager
from models.alert import Alert
from repositories.base import BaseRepository


async def periodic_alert_generator(
    manager: ConnectionManager, repository: BaseRepository, interval_seconds: int = 10
) -> None:
    gates = cycle(range(1, 5))

    try:
        for _ in count(1):
            gate = next(gates)
            alert = Alert(
                message="Intruder detected",
                location=f"Gate {gate}",
                timestamp=datetime.now(timezone.utc),
            )

            repository.add(alert)
            await manager.broadcast_json({"type": "alert", **alert.model_dump()})
            await asyncio.sleep(interval_seconds)
    except asyncio.CancelledError:
        raise
