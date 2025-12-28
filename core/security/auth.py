from datetime import timedelta
from typing import Any, MutableMapping, cast
from uuid import uuid4

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from redis.asyncio.client import Redis

from core.settings import settings
from utils.get_utc_now import get_utc_now

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/token",
    description="Use email as the username field",
)


def create_access_token(
    sub: str,
    extra_claims: dict[str, Any] | None = None,
    expires_delta: timedelta | None = None,
) -> str:

    if expires_delta:
        expire = get_utc_now() + expires_delta
    else:
        expire = get_utc_now() + timedelta(
            minutes=settings.access_token_expire_minutes,
        )

    if not extra_claims:
        extra_claims = {}

    payload = {
        "type": "access",
        "sub": sub,
        "jti": str(uuid4()),
        "iat": get_utc_now(),
        "exp": expire,
        **extra_claims,
    }

    encoded_jwt = jwt.encode(
        claims=cast(MutableMapping[str, Any], payload),
        key=settings.access_secret_key,
        algorithm=settings.algorithm,
    )

    return encoded_jwt


async def verify_access_token(redis: Redis, token: str) -> dict[str, Any]:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid or expired access token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload: dict[str, Any] = jwt.decode(
            token,
            settings.access_secret_key,
            algorithms=[settings.algorithm],
        )

        # Check, Is token block by jti
        jti: str | None = payload.get("jti")
        if await redis.get(f"blocklist:{jti}"):
            raise HTTPException(status_code=401, detail="Token revoked")

        # Check token type
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=401,
                detail="Invalid token type",
            )

        # Get auth subject detail
        if payload.get("sub") is None:
            raise credentials_exception

        # Return UUID instance
        return payload
    except JWTError:
        raise credentials_exception


def create_refresh_token(
    sub: str,
    extra_claims: dict[str, Any] | None = None,
    expires_delta: timedelta | None = None,
) -> str:

    if expires_delta:
        expire = get_utc_now() + expires_delta
    else:
        expire = get_utc_now() + timedelta(
            minutes=settings.refresh_token_expire_minutes,
        )

    if not extra_claims:
        extra_claims = {}

    payload = {
        "type": "refresh",
        "sub": sub,
        "jti": str(uuid4()),
        "iat": get_utc_now(),
        "exp": expire,
        **extra_claims,
    }

    encoded_jwt = jwt.encode(
        claims=cast(MutableMapping[str, Any], payload),
        key=settings.refresh_secret_key,
        algorithm=settings.algorithm,
    )

    return encoded_jwt


async def verify_refresh_token(redis: Redis, token: str) -> dict[str, Any]:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid or expired refresh token",
    )

    try:
        payload: dict[str, Any] = jwt.decode(
            token,
            settings.refresh_secret_key,
            algorithms=[settings.algorithm],
        )

        # Check, Is token block by jti
        jti: str | None = payload.get("jti")
        if await redis.get(f"blocklist:{jti}"):
            raise HTTPException(status_code=401, detail="Token revoked")

        # Check token type
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=401,
                detail="Invalid token type",
            )

        # Get auth subject detail
        if payload.get("sub") is None:
            raise credentials_exception

        # Return UUID instance
        return payload
    except JWTError:
        raise credentials_exception


async def revoke_token(
    redis: Redis,
    jti: str,
    exp: int,
) -> None:
    # seconds until expiry
    ttl = max(exp - int(get_utc_now().timestamp()), 0)

    # Cache jti to block token
    await redis.set(f"blocklist:{jti}", "1", ex=ttl)
