import bcrypt

from config.core.bcrypt import BcryptConfig


class Bcrypt:
    @staticmethod
    def hash_password(password: str) -> str:
        password_bytes = password.encode("utf-8")
        password_hash = bcrypt.hashpw(
            password_bytes, bcrypt.gensalt(BcryptConfig.ROUNDS)
        )

        return password_hash.decode("utf-8")

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
