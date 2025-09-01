from fastapi import APIRouter, Depends

from dependencies import get_alerts_repo, get_manager
from managers.connection_manager import ConnectionManager
from models.alert import Alert
from repositories.base import BaseRepository

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("/history", response_model=list[Alert])
async def get_alert_history(repository: BaseRepository = Depends(get_alerts_repo)):
    """Return last N alerts from the repository."""
    return repository.get_all()


@router.post("/", response_model=Alert)
async def post_alert(
    alert: Alert,
    repository: BaseRepository = Depends(get_alerts_repo),
    manager: ConnectionManager = Depends(get_manager),
):
    """Add a new alert manually and broadcast it."""
    repository.add(alert)
    await manager.broadcast_json({"type": "alert", **alert.model_dump()})
    return alert
