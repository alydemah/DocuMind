import contextlib
import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)

websocket_router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, channel: str):
        await websocket.accept()
        if channel not in self.active_connections:
            self.active_connections[channel] = []
        self.active_connections[channel].append(websocket)

    def disconnect(self, websocket: WebSocket, channel: str):
        if channel in self.active_connections:
            self.active_connections[channel].remove(websocket)
            if not self.active_connections[channel]:
                del self.active_connections[channel]

    async def broadcast(self, channel: str, message: dict):
        if channel in self.active_connections:
            for connection in self.active_connections[channel]:
                with contextlib.suppress(Exception):
                    await connection.send_json(message)


manager = ConnectionManager()


@websocket_router.websocket("/ws/processing/{document_id}")
async def processing_status(websocket: WebSocket, document_id: str):
    channel = f"processing:{document_id}"
    await manager.connect(websocket, channel)
    try:
        while True:
            data = await websocket.receive_text()
            logger.debug(f"Received on {channel}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, channel)


@websocket_router.websocket("/ws/chat/{conversation_id}")
async def chat_stream(websocket: WebSocket, conversation_id: str):
    channel = f"chat:{conversation_id}"
    await manager.connect(websocket, channel)
    try:
        while True:
            data = await websocket.receive_text()
            logger.debug(f"Received on {channel}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, channel)


async def send_processing_update(document_id: str, status: dict):
    channel = f"processing:{document_id}"
    await manager.broadcast(channel, status)


async def send_chat_chunk(conversation_id: str, chunk: str):
    channel = f"chat:{conversation_id}"
    await manager.broadcast(channel, {"type": "chunk", "content": chunk})


async def send_chat_done(conversation_id: str, response: dict):
    channel = f"chat:{conversation_id}"
    await manager.broadcast(channel, {"type": "done", **response})
