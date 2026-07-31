from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.app import AppConfig
from config.uvicorn import UvicornConfig
from core.redis import redis_client
from routes import router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await redis_client.ping()

    yield

    await redis_client.aclose()


api = FastAPI(
    title="Music Roulette Backend",
    debug=AppConfig.IS_DEVELOPMENT_ENVIRONMENT,
    lifespan=lifespan,
)

if AppConfig.IS_DEVELOPMENT_ENVIRONMENT:
    api.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

api.include_router(router)

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

app.mount("/api", api)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=UvicornConfig.HOST,
        port=UvicornConfig.PORT,
        reload=IS_DEVELOPMENT_ENVIRONMENT,
    )
