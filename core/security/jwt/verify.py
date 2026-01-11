from logging import getLogger
from typing import Any

from jose import ExpiredSignatureError, jwt
from jose import JWTError as JoseJWTError
from redis.asyncio.client import Redis

from core.config.settings import settings

from .exceptions import ExpiredTokenError, InvalidTokenError, RevokedTokenError
from .revocation import is_token_revoked

logger = getLogger(__name__)


async def _verify_jwt(
    *, redis: Redis, sub: str, token: str, secret_key: str, algorithm: str
) -> dict[str, Any]:
    try:
        claims = jwt.decode(
            token=token,
            key=secret_key,
            algorithms=[algorithm],
        )
    except ExpiredSignatureError as error:
        logger.debug("JWT verification failed: token expired", exc_info=True)
        raise ExpiredTokenError(
            code="expire_token", detail="Jwt token signature expire"
        ) from error
    except JoseJWTError as error:
        logger.debug("JWT verification failed: invalid token", exc_info=True)
        raise InvalidTokenError(
            code="invalid_jwt_token", detail="Invalid jwt token"
        ) from error

    # Check required claims
    required_claims = {"sub", "exp", "iat", "jti"}
    if not required_claims.issubset(claims):
        logger.debug("JWT verification failed: missing required claims")
        raise InvalidTokenError(
            code="invalid_jwt_token",
            detail="Jwt verification failed by missing required claims",
        )

    # Check subject
    if claims["sub"] != sub:
        logger.debug(
            "JWT verification failed: subject mismatch " "(expected=%s, actual=%s)",
            sub,
            claims.get("sub"),
        )
        raise InvalidTokenError(
            code="invalid_jwt_token",
            detail="Jwt verification failed because subject mismatch",
        )

    # Check, Is revoked by client
    if await is_token_revoked(redis=redis, jti=claims["jti"]):
        logger.debug("Jwt verification failed: token revoked")
        raise RevokedTokenError(
            code="token_revoked",
            detail="Jwt verification failed because token revoked",
        )

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
