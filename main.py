import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from managers.connection_manager import ConnectionManager
from repositories.alert import AlertRepository
from routes.alert import router as alerts_router
from routes.websocket import router as websocket_router
from services.alert_generator import periodic_alert_generator

manager = ConnectionManager()
alerts = AlertRepository()


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    # Startup
    task = asyncio.create_task(periodic_alert_generator(manager, alerts))

    # App is running
    yield

    # Shutdown
    if task:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass


app = FastAPI(title="WebSocket Alert Server", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=500)
app.include_router(alerts_router)
app.include_router(websocket_router)
