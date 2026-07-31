import secrets
from uuid import UUID, uuid4

from fastapi import APIRouter, WebSocketDisconnect
from pydantic import ValidationError

from core.bcrypt import Bcrypt
from core.redis import redis_client
from schemas.response.v1.lobby import *
from schemas.v1.lobby import BaseLobbySchema
from websockets_managers.v1.lobby import lobby_connection_manager

router = APIRouter(prefix="/lobby")

LOBBY_EXPIRATION = 3600 * 6  # 6 hours


@router.post("/")
async def create_lobby() -> LobbyCreateResponse:
    uuid = uuid4()
    token = secrets.token_urlsafe(32)
    await redis_client.set(str(uuid), Bcrypt.hash_password(token), ex=LOBBY_EXPIRATION)
    return LobbyCreateResponse(lobby_id=uuid, token=token)


@router.get("/{lobby_id:str}")  # TODO: Remove this route, only for testing purposes
async def get_lobby(lobby_id: UUID):
    lobby = await redis_client.get(str(lobby_id))

    return {"lobby_id": lobby_id, "exists": bool(lobby)}


@router.websocket("/{lobby_id:str}")
async def websocket_endpoint(websocket, lobby_id: UUID, username: str) -> None:
    lobby = await redis_client.get(str(lobby_id))

    if lobby is None:
        await websocket.accept()

        await lobby_connection_manager.send(
            websocket=websocket,
            message=LobbyErrorResponse(
                lobby_id=lobby_id,
                error="Lobby not found",
                message="The lobby you are trying to join does not exist",
            ),
        )

        await websocket.close(code=4404, reason="Lobby not found")
        return

    await lobby_connection_manager.connect(lobby_id, websocket)

    await lobby_connection_manager.send(
        websocket=websocket, message=LobbyJoinResponse(username=username)
    )

    try:
        while True:
            raw_message = await websocket.receive_text()

            try:
                request = BaseLobbySchema.model_validate_json(raw_message)
            except ValidationError:
                await lobby_connection_manager.send(
                    websocket=websocket,
                    message=LobbyErrorResponse(
                        lobby_id=lobby_id,
                        error="Invalid request",
                        message="The request you sent is invalid",
                    ),
                )
                continue

            response = BaseLobbySchema(data=request.data)

            await lobby_connection_manager.broadcast(
                lobby_id, response, sender=websocket
            )

    except WebSocketDisconnect:
        lobby_connection_manager.disconnect(lobby_id, websocket)
