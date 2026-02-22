from datetime import timedelta
from typing import Any, Mapping
from uuid import uuid4

from jose import jwt

from app.shared.datetime.utc_now import get_utc_now

# =============================================================================
# Jwt Factory Class That Create Jwt Tokens.
# =============================================================================


class JwtFactory:
    @staticmethod
    def create_token(
        *,
        claims: Mapping[str, Any],
        subject: str,
        secret_key: str,
        algorithm: str,
        expires_in: timedelta,
    ) -> str:
        utc_now = get_utc_now()

        payload: dict[str, Any] = {
            **claims,
            "sub": subject,
            "jti": str(uuid4()),
            "iat": utc_now,
            "exp": utc_now + expires_in,
        }

        return jwt.encode(
            claims=payload,
            key=secret_key,
            algorithm=algorithm,
        )
