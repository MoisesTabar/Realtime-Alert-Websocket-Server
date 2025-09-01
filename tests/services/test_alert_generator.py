import asyncio

from services.alert_generator import periodic_alert_generator


class FakeManager:
    def __init__(self):
        self.broadcasts = []
        self._first_event = asyncio.Event()

    async def broadcast_json(self, data: dict):
        self.broadcasts.append(data)
        if not self._first_event.is_set():
            self._first_event.set()


class FakeRepo:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)


def test_periodic_alert_generator_generates_and_broadcasts_then_cancellable():
    async def run():
        m = FakeManager()
        r = FakeRepo()
        task = asyncio.create_task(periodic_alert_generator(m, r, interval_seconds=0))
        # Wait for first broadcast
        await asyncio.wait_for(m._first_event.wait(), timeout=2)
        # After first event, cancel the task
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

        assert len(r.items) >= 1
        # Broadcast contains type 'alert' and fields
        assert m.broadcasts[0]["type"] == "alert"
        assert "message" in m.broadcasts[0]
        assert "location" in m.broadcasts[0]
        assert "timestamp" in m.broadcasts[0]

    asyncio.run(run())
