from typing import Protocol

# =============================================================================
# Hasher protocol.
# =============================================================================


class Hasher[T](Protocol):
    def hash(self, value: T) -> str: ...
    def verify(self, value: T, hashed: str) -> bool: ...


# =============================================================================
# Encryption protocol.
# =============================================================================


class Encryptor[T](Protocol):
    def encrypt(self, value: T) -> bytes: ...
    def decrypt(self, value: bytes) -> T: ...
