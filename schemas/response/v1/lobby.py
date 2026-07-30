from uuid import UUID

from pydantic import BaseModel


class LobbyCreateResponse(BaseModel):
    lobby_id: UUID
    token: str
