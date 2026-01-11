from datetime import timedelta
from typing import Any
from uuid import uuid4

from jose import jwt

from core.config.settings import settings

from ...utils.time import time


def _create_jwt(
    *,
    claims: dict[str, Any],
    subject: str,
    secret_key: str,
    algorithm: str,
    expires_in: timedelta,
) -> str:
    utc_now = time.utc_now()
    payload = {
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
