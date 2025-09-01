import uuid
from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class Alert(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    message: str
    location: str
    timestamp: datetime

    @field_validator("timestamp", mode="before")
    def ensure_datetime(cls, value):
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError as e:
                raise ValueError(f"Invalid timestamp format: {value}") from e
        raise TypeError("timestamp must be a datetime or an ISO8601 string")
