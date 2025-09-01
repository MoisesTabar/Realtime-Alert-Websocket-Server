from dataclasses import dataclass

from models.message import ChatMessage
from repositories.base import BaseRepository


@dataclass(slots=True)
class ChatRepository(BaseRepository[ChatMessage]):
    maxlen: int = 100
