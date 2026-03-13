"""WebSocket connection manager and broadcast."""

from __future__ import annotations

from typing import Any, Dict, Set

import orjson
from fastapi import WebSocket


class ConnectionManager:
    """Manages WebSocket connections and broadcasts state to all clients."""

    def __init__(self) -> None:
        self._connections: Set[WebSocket] = set()

    async def connect(self, ws: WebSocket) -> None:
        await ws.accept()
        self._connections.add(ws)

    def disconnect(self, ws: WebSocket) -> None:
        self._connections.discard(ws)

    async def broadcast(self, data: Dict[str, Any]) -> None:
        """Serialize once with orjson, send to all connected clients."""
        if not self._connections:
            return

        payload = orjson.dumps(data).decode("utf-8")
        dead: list[WebSocket] = []

        for ws in self._connections:
            try:
                await ws.send_text(payload)
            except Exception:
                dead.append(ws)

        for ws in dead:
            self._connections.discard(ws)

    @property
    def client_count(self) -> int:
        return len(self._connections)
