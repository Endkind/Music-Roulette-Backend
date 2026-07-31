from collections import defaultdict
from typing import Dict, List
from uuid import UUID

from fastapi import WebSocket
from pydantic import BaseModel

from core.redis import redis_client


class LobbyConnectionManager:
    def __init__(self) -> None:
        self._connections: Dict[UUID, set[WebSocket]] = defaultdict(set)

    async def connect(self, lobby_id: UUID, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections[lobby_id].add(websocket)

    def disconnect(self, lobby_id: UUID, websocket: WebSocket) -> None:
        connections = self._connections.get(lobby_id)

        if connections is None:
            return

        connections.discard(websocket)

        if not connections:  # TODO: Replace with 15m timeout
            self._connections.pop(lobby_id, None)
            redis_client.delete(str(lobby_id))

    async def send(
        self,
        websocket: WebSocket,
        message: BaseModel,
    ) -> None:
        await websocket.send_json(message.model_dump(mode="json"))

    async def broadcast(
        self,
        lobby_id: UUID,
        message: BaseModel,
        sender: WebSocket | None = None,
    ) -> None:
        connections = self._connections.get(lobby_id)

        if connections is None:
            return

        disconnected_connections: List[WebSocket] = []
        payload = message.model_dump(mode="json")

        for connection in connections.copy():
            if connection is sender:
                continue

            try:
                await connection.send_json(payload)
            except RuntimeError:
                disconnected_connections.append(connection)

        for disconnected_connection in disconnected_connections:
            self.disconnect(lobby_id, disconnected_connection)


lobby_connection_manager = LobbyConnectionManager()
