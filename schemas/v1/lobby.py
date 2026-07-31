from typing import Annotated, Any

from pydantic import StringConstraints, field_validator

from config.v1.lobby import LobbyConfig
from enums.v1.lobby import LobbyRequestType
from schemas.websocket.v1.lobby import LobbyWebSocketSchema

Username = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=50,
    ),
]


class BaseLobbySchema(LobbyWebSocketSchema):
    type: LobbyRequestType
    username: Username
    data: dict[str, Any]

    @field_validator("username")
    @classmethod
    def validate_username(cls, username: str) -> str:
        if username.casefold() in (
            name.casefold() for name in LobbyConfig.FORBIDDEN_USERNAMES
        ):
            raise ValueError(
                "This username is not allowed. Please choose a different username."
            )

        return username
