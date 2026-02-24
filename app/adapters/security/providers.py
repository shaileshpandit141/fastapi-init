from app.core.config import get_settings

from .encryption import FernetEncryptor
from .hashing import Argon2Hasher

# =============================================================================
# Getting env settings.
# =============================================================================

settings = get_settings()

# =============================================================================
# Function that return Argon2Hasher instance.
# =============================================================================


def get_hasher() -> Argon2Hasher:
    return Argon2Hasher()


# =============================================================================
# Function that return FernetEncryptor instance.
# =============================================================================


def get_encryptor() -> FernetEncryptor:
    return FernetEncryptor(settings.encryption.KEY.encode())
