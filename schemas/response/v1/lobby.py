from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class LobbyCreateResponse(BaseModel):
    lobby_id: UUID
    token: str


class LobbyErrorResponse(BaseModel):
    lobby_id: UUID
    error: str
    message: str


class LobbyJoinResponse(BaseModel):
    username: str


# region Websocket
class WebSocketSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")


class LobbyMessageRequest(WebSocketSchema):
    type: Literal["message"]
    data: dict[str, Any]


class LobbyConnectedResponse(WebSocketSchema):
    type: Literal["connected"] = "connected"
    lobby_id: UUID


class LobbyMessageResponse(WebSocketSchema):
    type: Literal["message"] = "message"
    lobby_id: UUID
    data: dict[str, Any]


# endregion
