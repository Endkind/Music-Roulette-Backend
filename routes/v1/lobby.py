import secrets
from uuid import uuid4

from fastapi import APIRouter

from core.bcrypt import Bcrypt
from core.redis import redis_client
from schemas.response.v1.lobby import *

router = APIRouter(prefix="/lobby")

LOBBY_EXPIRATION = 3600 * 6  # 6 hours


@router.post("/")
async def create_lobby():
    uuid = uuid4()
    token = secrets.token_urlsafe(32)
    await redis_client.set(f"{uuid}", Bcrypt.hash_password(token), ex=LOBBY_EXPIRATION)
    return LobbyCreateResponse(lobby_id=uuid, token=token)
