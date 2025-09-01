from datetime import datetime, timezone
from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    sender: str
    message: str
    timestamp: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )