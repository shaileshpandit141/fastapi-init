from datetime import timedelta
from typing import Any, Literal
from uuid import uuid4

from jose import jwt

from core.settings import settings
from utils.get_utc_now import get_utc_now


def create_token(claims: dict[str, Any], key: str, algorithm: str) -> str:
    """Create a JWT token with given claims, key, and algorithm."""

    return jwt.encode(
        claims=claims,
        key=key,
        algorithm=algorithm,
    )


def create_jwt_token(
    sub: Literal["access", "refresh"],
    claims: dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    """Create a JWT token with specified subject and claims."""

    now = get_utc_now()

    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.access_token_expire_minutes)

    payload = {
        "sub": sub,
        "jti": str(uuid4()),
        "iat": now,
        "exp": expire,
        **claims,
    }

    if sub == "access":
        return create_token(
            claims=payload,
            key=settings.access_token_secret_key,
            algorithm=settings.algorithm,
        )
    elif sub == "refresh":
        return create_token(
            claims=payload,
            key=settings.refresh_token_secret_key,
            algorithm=settings.algorithm,
        )
    else:
        raise ValueError("Invalid subject type for JWT token")
