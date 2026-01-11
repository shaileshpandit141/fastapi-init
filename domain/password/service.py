from passlib.context import CryptContext


class PasswordService:
    def __init__(self) -> None:
        self.crypto = CryptContext(schemes=["argon2"], deprecated="auto")

    def hash(self, *, password: str | bytes) -> str:
        return self.crypto.hash(secret=password)

    def verify(
        self, *, plain_password: str | bytes, hashed_password: str | bytes
    ) -> bool:
        return self.crypto.verify(secret=plain_password, hash=hashed_password)
