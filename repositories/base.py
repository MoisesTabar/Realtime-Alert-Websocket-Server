from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Generic, TypeVar

T = TypeVar("T")


@dataclass(slots=True)
class BaseRepository(Generic[T]):
    maxlen: int
    _items: Deque[T] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._items = deque(maxlen=self.maxlen)

    def add(self, item: T) -> None:
        self._items.appendleft(item)

    def get_all(self) -> list[T]:
        return list(self._items)
