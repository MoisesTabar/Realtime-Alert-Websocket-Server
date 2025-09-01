from datetime import datetime
from pydantic import BaseModel, Field, field_validator
import uuid

class Alert(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    message: str
    location: str
    timestamp: datetime

    @field_validator("timestamp", pre=True)
    def ensure_datetime(cls, value: str):
        return datetime.fromisoformat(value.replace("Z", "+00:00"))