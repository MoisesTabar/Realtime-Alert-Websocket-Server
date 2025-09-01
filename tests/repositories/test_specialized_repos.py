from datetime import datetime, timezone

from models.alert import Alert
from models.message import ChatMessage
from repositories.alert import AlertRepository
from repositories.chat import ChatRepository


def test_alert_repository_default_maxlen_and_storage():
    repo = AlertRepository()
    assert repo.maxlen == 10
    a = Alert(message="m", location="L", timestamp=datetime.now(timezone.utc))
    repo.add(a)
    assert repo.get_all() == [a]


def test_chat_repository_default_maxlen_and_storage():
    repo = ChatRepository()
    assert repo.maxlen == 100
    m = ChatMessage(sender="s", message="hi")
    repo.add(m)
    assert repo.get_all() == [m]
