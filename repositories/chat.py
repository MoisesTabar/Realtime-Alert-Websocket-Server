from collections import deque
from dataclasses import dataclass, field

from models.message import ChatMessage


@dataclass(slots=True)
class ChatRepository:
    """
    In-memory store for chat messages with fixed max length.
    """

    maxlen: int = 100
    _chats: deque = field(default_factory=lambda: deque(maxlen=100))

    def add(self, chat: ChatMessage) -> None:
        self._chats.appendleft(chat)

    def get_all(self) -> list[ChatMessage]:
        return list(self._chats)
