import os
from typing import Final, Optional


class RedisConfig:
    HOST: Final[str] = os.getenv("REDIS_HOST", "localhost")
    PORT: Final[int] = int(os.getenv("REDIS_PORT", 6379))
    DATABASE: Final[int] = int(os.getenv("REDIS_DATABASE", 0))
    PASSWORD: Final[Optional[str]] = os.getenv("REDIS_PASSWORD")

    URL: Final[str] = os.getenv("REDIS_URL", f"redis://{HOST}:{PORT}/{DATABASE}")
