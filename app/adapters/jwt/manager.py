from datetime import timedelta
from enum import StrEnum
from typing import Any, Mapping

from redis.asyncio.client import Redis

from app.core.config import get_settings

from .blocklist import JwtBlocklist
from .factory import JwtFactory
from .verifier import JwtVerifier

# =============================================================================
# Token Constants
# =============================================================================


ACCESS_SUBJECT = "access"
REFRESH_SUBJECT = "refresh"


class TokenTypeEnum(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"


# =============================================================================
# Creating Settings Instance.
# =============================================================================

settings = get_settings()


# =============================================================================
# Jwt Token Manager Class.
# =============================================================================


class JwtTokenManager:
    def __init__(self, redis: Redis) -> None:
        self.blocklist = JwtBlocklist(redis)
        self.verifier = JwtVerifier(self.blocklist)
        self.secret_key = settings.jwt.SECRET_KEY
        self.algorithm = settings.jwt.ALGORITHM

    def create_token(self, type: TokenTypeEnum, claims: Mapping[str, Any]) -> str:
        if type == TokenTypeEnum.ACCESS:
            return self.create_access_token(claims)
        elif type == TokenTypeEnum.REFRESH:
            return self.create_refresh_token(claims)
        else:
            raise ValueError("Invalid token type")

    def create_access_token(self, claims: Mapping[str, Any]) -> str:
        return JwtFactory.create_token(
            claims=claims,
            subject=ACCESS_SUBJECT,
            secret_key=self.secret_key,
            algorithm=self.algorithm,
            expires_in=timedelta(
                minutes=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES,
            ),
        )

    def create_refresh_token(self, claims: Mapping[str, Any]) -> str:
        return JwtFactory.create_token(
            claims=claims,
            subject=REFRESH_SUBJECT,
            secret_key=self.secret_key,
            algorithm=self.algorithm,
            expires_in=timedelta(
                minutes=settings.jwt.REFRESH_TOKEN_EXPIRE_MINUTES,
            ),
        )

    async def verify_access_token(self, token: str) -> dict[str, Any]:
        return await self.verifier.verify_token(
            token=token,
            expected_sub=ACCESS_SUBJECT,
            secret_key=self.secret_key,
            algorithm=self.algorithm,
        )

    async def verify_refresh_token(self, token: str) -> dict[str, Any]:
        return await self.verifier.verify_token(
            token=token,
            expected_sub=REFRESH_SUBJECT,
            secret_key=self.secret_key,
            algorithm=self.algorithm,
        )

    async def verify_token(self, type: TokenTypeEnum, token: str) -> dict[str, Any]:
        if type == TokenTypeEnum.ACCESS:
            return await self.verify_access_token(token)
        elif type == TokenTypeEnum.REFRESH:
            return await self.verify_refresh_token(token)
        else:
            raise ValueError("Invalid token type")

    async def revoke_token(self, jti: str, exp: int) -> None:
        await self.blocklist.revoke(jti=jti, exp=exp)
