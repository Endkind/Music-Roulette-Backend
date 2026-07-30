from enum import Enum
from typing import Final


class AppEnvironment(Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"


class AppConfig:
    ENV: Final[AppEnvironment] = AppEnvironment.DEVELOPMENT
