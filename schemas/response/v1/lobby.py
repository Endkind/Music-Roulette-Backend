from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel

from schemas.websocket.v1.lobby import LobbyWebSocketSchema


class LobbyCreateResponse(BaseModel):
    lobby_id: UUID
    token: str


class LobbyErrorResponse(BaseModel):
    lobby_id: UUID
    error: str
    message: str


class LobbyJoinResponse(BaseModel):
    username: str
