from typing import Final

from passlib.context import CryptContext


class PasswordHasher:
    _context: Final[CryptContext] = CryptContext(
        schemes=["argon2"],
        deprecated="auto",
    )

    def hash_password(self, password: str | bytes) -> str:
        return self._context.hash(password)

    def verify_password(
        self, plain_password: str | bytes, hashed_password: str | bytes
    ) -> bool:
        return self._context.verify(
            plain_password,
            hashed_password,
        )

    def verify_and_update(
        self, plain_password: str | bytes, hashed_password: str
    ) -> tuple[bool, str | None]:
        verified, new_hash = self._context.verify_and_update(
            plain_password,
            hashed_password,
        )
        return verified, new_hash
