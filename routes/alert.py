from fastapi import APIRouter, Depends

from controllers.alert import AlertController
from dependencies import get_alert_controller
from models.alert import Alert

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("/history", response_model=list[Alert])
async def get_alert_history(
    controller: AlertController = Depends(get_alert_controller),
):
    """Return last N alerts from the repository."""
    return controller.get_history()


@router.post("/", response_model=Alert)
async def post_alert(
    alert: Alert,
    controller: AlertController = Depends(get_alert_controller),
):
    """Add a new alert manually and broadcast it."""
    return await controller.post_alert(alert)
