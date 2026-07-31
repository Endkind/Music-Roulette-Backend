import os
from typing import Final


class UvicornConfig:
    HOST: Final[str] = os.getenv("HOST", "0.0.0.0")
    PORT: Final[int] = int(os.getenv("PORT", 8000))
