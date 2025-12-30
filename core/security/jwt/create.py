from datetime import timedelta
from typing import Any
from uuid import uuid4

from jose import jwt

from core.config import settings
from utils.get_utc_now import get_utc_now


def _create_jwt(
    *,
    claims: dict[str, Any],
    subject: str,
    secret_key: str,
    algorithm: str,
    expires_in: timedelta,
) -> str:
    payload = {
        **claims,
        "sub": subject,
        "jti": str(uuid4()),
        "iat": get_utc_now(),
        "exp": get_utc_now(add=expires_in),
    }

    return jwt.encode(
        claims=payload,
        key=secret_key,
        algorithm=algorithm,
    )


def create_access_token(claims: dict[str, Any]) -> str:
    return _create_jwt(
        claims=claims,
        subject="access",
        secret_key=settings.access_token_secret_key,
        algorithm=settings.algorithm,
        expires_in=timedelta(minutes=settings.access_token_expire_minutes),
    )


def create_refresh_token(claims: dict[str, Any]) -> str:
    return _create_jwt(
        claims=claims,
        subject="refresh",
        secret_key=settings.refresh_token_secret_key,
        algorithm=settings.algorithm,
        expires_in=timedelta(minutes=settings.refresh_token_expire_minutes),
    )
