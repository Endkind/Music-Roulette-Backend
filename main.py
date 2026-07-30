from typing import Final

from fastapi import FastAPI
import uvicorn
from config.uvicorn import UvicornConfig
from config.app import AppConfig, AppEnvironment

DEBUG: Final[bool] = AppConfig.ENV == AppEnvironment.DEVELOPMENT

app = FastAPI(
    title="Music Roulette Backend",
    debug=DEBUG,
)

if __name__ == "__main__":
    uvicorn.run("main:app", host=UvicornConfig.HOST, port=UvicornConfig.PORT, reload=DEBUG)