import asyncio

from starlette.websockets import WebSocketState

from managers.connection_manager import ConnectionManager


class FakeWebSocket:
    def __init__(self, connected: bool = True, fail_send: bool = False):
        self.application_state = (
            WebSocketState.CONNECTED if connected else WebSocketState.DISCONNECTED
        )
        self.client_state = (
            WebSocketState.CONNECTED if connected else WebSocketState.DISCONNECTED
        )
        self.accepted = False
        self.sent = []
        self.fail_send = fail_send

    async def accept(self):
        self.accepted = True
        self.application_state = WebSocketState.CONNECTED
        self.client_state = WebSocketState.CONNECTED

    async def send_json(self, data):
        if self.fail_send:
            raise RuntimeError("send failure")
        self.sent.append(data)


def test_connect_and_disconnect_manage_sets_and_locks():
    async def run():
        m = ConnectionManager()
        ws = FakeWebSocket()
        await m.connect(ws)  # should accept and add
        assert ws in m.active_connections
        assert ws in m._locks and isinstance(m._locks[ws], asyncio.Lock)

        m.disconnect(ws)
        assert ws not in m.active_connections
        assert ws not in m._locks

    asyncio.run(run())


def test_broadcast_json_sends_only_to_connected():
    async def run():
        m = ConnectionManager()
        ws1 = FakeWebSocket(connected=True)
        ws2 = FakeWebSocket(connected=False)  # should be skipped and removed
        await m.connect(ws1)
        # Manually add ws2 without connect to simulate stale/closed socket
        m.active_connections.add(ws2)

        await m.broadcast_json({"x": 1})

        assert ws1.sent == [{"x": 1}]
        assert ws2 not in m.active_connections  # removed due to not connected

    asyncio.run(run())


def test_broadcast_json_removes_on_send_exception():
    async def run():
        m = ConnectionManager()
        ws = FakeWebSocket(connected=True, fail_send=True)
        await m.connect(ws)

        await m.broadcast_json({"y": 2})

        # send_json raised -> socket removed
        assert ws not in m.active_connections
        # lock cleaned up
        assert ws not in m._locks

    asyncio.run(run())
