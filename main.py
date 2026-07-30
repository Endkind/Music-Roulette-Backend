from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Final

import uvicorn
from fastapi import FastAPI

from config.app import AppConfig, AppEnvironment
from config.uvicorn import UvicornConfig
from core.redis import redis_client
from routes import router

DEBUG: Final[bool] = AppConfig.ENV == AppEnvironment.DEVELOPMENT


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await redis_client.ping()

    yield

    await redis_client.aclose()


api = FastAPI(title="Music Roulette Backend", debug=DEBUG, lifespan=lifespan)

api.include_router(router)

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

app.mount("/api", api)

if __name__ == "__main__":
    uvicorn.run(
        "main:app", host=UvicornConfig.HOST, port=UvicornConfig.PORT, reload=DEBUG
    )
