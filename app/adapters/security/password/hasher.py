from typing import Final
from passlib.context import CryptContext


class PasswordHasher:
    _context: Final[CryptContext] = CryptContext(
        schemes=["argon2"],
        deprecated="auto",
    )

    def hash_password(self, password: str | bytes) -> str:
        return self._context.hash(password)

    def verify(self, password: str | bytes, hashed_password: str) -> bool:
        return self._context.verify(password, hashed_password)

    def verify_and_update(
        self,
        password: str | bytes,
        hashed_password: str,
    ) -> tuple[bool, str | None]:
        return self._context.verify_and_update(password, hashed_password)
