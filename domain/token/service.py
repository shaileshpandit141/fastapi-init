from datetime import timedelta
from logging import getLogger
from typing import Any
from uuid import uuid4

from jose import ExpiredSignatureError, jwt
from jose import JWTError as JoseJWTError
from redis.asyncio.client import Redis

from core.settings import settings
from core.utils.time import time

from .exceptions import ExpiredTokenError, InvalidTokenError, RevokedTokenError

logger = getLogger(__name__)


class BaseJwtToken:
    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    def create_jwt(
        self,
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

    async def revoke_token(self, *, jti: str, exp: int) -> None:
        ttl = max(exp - int(time.utc_now().timestamp()), 0)  # seconds until expiry
        if ttl > 0:
            await self.redis.set(f"blocklist:{jti}", "1", ex=ttl)

    async def is_token_revoked(self, *, jti: str) -> bool:
        if await self.redis.get(f"blocklist:{jti}"):
            return True
        return False

    async def verify_jwt(
        self, *, sub: str, token: str, secret_key: str, algorithm: str
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
        if await self.is_token_revoked(jti=claims["jti"]):
            logger.debug("Jwt verification failed: token revoked")
            raise RevokedTokenError(
                code="token_revoked",
                detail="Jwt verification failed because token revoked",
            )

        return claims


class JwtTokenService(BaseJwtToken):
    def __init__(self, redis: Redis) -> None:
        super().__init__(redis)

    def create_access_token(self, *, claims: dict[str, Any]) -> str:
        return self.create_jwt(
            claims=claims,
            subject="access",
            secret_key=settings.access_token_secret_key,
            algorithm=settings.algorithm,
            expires_in=timedelta(minutes=settings.access_token_expire_minutes),
        )

    def create_refresh_token(self, *, claims: dict[str, Any]) -> str:
        return self.create_jwt(
            claims=claims,
            subject="refresh",
            secret_key=settings.refresh_token_secret_key,
            algorithm=settings.algorithm,
            expires_in=timedelta(minutes=settings.refresh_token_expire_minutes),
        )

    async def verify_access_token(self, *, token: str) -> dict[str, Any]:
        return await self.verify_jwt(
            sub="access",
            token=token,
            secret_key=settings.access_token_secret_key,
            algorithm=settings.algorithm,
        )

    async def verify_refresh_token(self, *, token: str) -> dict[str, Any]:
        return await self.verify_jwt(
            sub="refresh",
            token=token,
            secret_key=settings.refresh_token_secret_key,
            algorithm=settings.algorithm,
        )
