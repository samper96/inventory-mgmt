"""
Websocket API Router.

Provides real-time product stock updates using WebSockets.
"""

import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from websocket_manager import WebSocketConnectionManager

router = APIRouter(prefix="/ws", tags=["WebSocket"])
logger = logging.getLogger(__name__)

connection_manager = WebSocketConnectionManager()


@router.websocket("/stock")
async def stock_updates(websocket: WebSocket):
    """
    WebSocket endpoint for real-time product stock updates.

    Clients can send and receive stock update messages.

    Args:
        websocket (WebSocket): WebSocket connection instance.
    """
    await connection_manager.connect(websocket)
    client = websocket.client
    logger.info("WebSocket connection accepted from %s:%s" % (str(client.host), str(client.port)))
    try:
        while True:
            data = await websocket.receive_text()
            logger.debug("Received stock data.")

            await connection_manager.broadcast("Received stock update: %s" % data)
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
        logger.info("WebSocket client disconnected: %s:%s" % (str(client.host), str(client.port)))
    except Exception as e:
        error_msg = "An error occurred: %s" % (str(e))
        logger.error(error_msg)
        await websocket.send_text(error_msg)
        # Close the connection on unexpected error
        await websocket.close()
