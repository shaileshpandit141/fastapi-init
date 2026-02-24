from cryptography.fernet import Fernet

from .interfaces import Encryptor

# =============================================================================
# Encryptor class.
# =============================================================================


class FernetEncryptor(Encryptor[str]):
    def __init__(self, key: bytes) -> None:
        self._fernet = Fernet(key)

    def encrypt(self, value: str) -> bytes:
        return self._fernet.encrypt(value.encode())

    def decrypt(self, value: bytes) -> str:
        return self._fernet.decrypt(value).decode()
