from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from .interfaces import Hasher

# =============================================================================
# Argon2 Hasher class.
# =============================================================================


class Argon2Hasher(Hasher[str]):
    def __init__(self) -> None:
        self._hasher = PasswordHasher(
            time_cost=3,
            memory_cost=65536,
            parallelism=4,
        )

    def hash(self, value: str) -> str:
        return self._hasher.hash(value)

    def verify(self, value: str, hashed: str) -> bool:
        try:
            return self._hasher.verify(hashed, value)
        except VerifyMismatchError:
            return False
