import os
from enum import Enum
from typing import Final


class AppEnvironment(Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"


def get_environment() -> AppEnvironment:
    env = os.getenv("ENV", AppEnvironment.DEVELOPMENT.value)
    try:
        return AppEnvironment(env)
    except ValueError:
        return AppEnvironment.PRODUCTION


class AppConfig:
    ENV: Final[AppEnvironment] = get_environment()
