from typing import Any

from jose import ExpiredSignatureError, jwt
from jose import JWTError as JoseJWTError
from redis.asyncio.client import Redis

from core.config import settings
from core.security.jwt.exceptions import (
    ExpiredTokenError,
    InvalidTokenError,
    RevokedTokenError,
)
from core.security.jwt.revocation import is_token_revoked


async def _verify_jwt(
    *,
    redis: Redis,
    sub: str,
    token: str,
    secret_key: str,
    algorithm: str,
) -> dict[str, Any]:
    try:
        claims = jwt.decode(
            token=token,
            key=secret_key,
            algorithms=[algorithm],
        )
    except ExpiredSignatureError:
        raise ExpiredTokenError()
    except JoseJWTError:
        raise InvalidTokenError()

    # Check required claims
    required_claims = {"sub", "exp", "iat", "jti"}
    if not required_claims.issubset(claims):
        raise InvalidTokenError()

    # Check subject
    if claims["sub"] != sub:
        raise InvalidTokenError()

    # Check, Is revoked by client
    if await is_token_revoked(redis=redis, jti=claims["jti"]):
        raise RevokedTokenError()

    return claims


async def verify_access_token(redis: Redis, token: str) -> dict[str, Any]:
    return await _verify_jwt(
        redis=redis,
        sub="access",
        token=token,
        secret_key=settings.access_token_secret_key,
        algorithm=settings.algorithm,
    )


async def verify_refresh_token(redis: Redis, token: str) -> dict[str, Any]:
    return await _verify_jwt(
        redis=redis,
        sub="refresh",
        token=token,
        secret_key=settings.refresh_token_secret_key,
        algorithm=settings.algorithm,
    )
