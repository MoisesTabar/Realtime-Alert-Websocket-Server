import asyncio
import logging
from datetime import datetime, timezone
from itertools import cycle

from managers.connection_manager import ConnectionManager
from models.alert import Alert
from repositories.base import BaseRepository


async def periodic_alert_generator(
    manager: ConnectionManager, repository: BaseRepository, interval_seconds: int = 10
) -> None:
    logging.info("Generating alerts...")
    gates = cycle(range(0, 5))

    try:
        while True:
            gate = next(gates)
            alert = Alert(
                message="Intruder detected",
                location=f"Gate {gate}",
                timestamp=datetime.now(timezone.utc),
            )

            repository.add(alert)
            await manager.broadcast_json(
                {"type": "alert", **alert.model_dump(mode="json")}
            )
            logging.info(f"Alert generated: {alert.id}")
            await asyncio.sleep(interval_seconds)
    except asyncio.CancelledError as e:
        logging.error("Alert generator cancelled", exc_info=e)
        raise
