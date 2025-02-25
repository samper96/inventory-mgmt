"""
WebSocket Connection Manager.

Maintains a list of active WebSocket connections and brodcasts messages to all.
"""

import logging
from typing import List
from fastapi import WebSocket

logger = logging.getLogger(__name__)


class WebSocketConnectionManager:
    def __init__(self):
        """Constructor for WebSocketConnectionManager."""
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Add `websocket` to the list of active WebSocket connections."""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Remove `websocket` from the list of active WebSocket connections."""
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        """Send `message` to all active WebSocket connections."""
        logger.info("Broadcasting: %s" % message)
        for connection in self.active_connections:
            await connection.send_text(message)
