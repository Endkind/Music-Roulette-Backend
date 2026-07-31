from pydantic import BaseModel, ConfigDict


class LobbyWebSocketSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")
