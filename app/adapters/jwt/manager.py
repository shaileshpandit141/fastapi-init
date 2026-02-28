from datetime import timedelta
from enum import StrEnum
from typing import Any, Mapping

from redis.asyncio.client import Redis

from app.core.config import get_settings

from .blacklist import JwtBlacklist
from .factory import JwtFactory
from .verifier import JwtVerifier

# =============================================================================
# Token Constants
# =============================================================================


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
        self.blacklist = JwtBlacklist(redis)
        self.verifier = JwtVerifier(self.blacklist)
        self.secret_key = settings.jwt.SECRET_KEY
        self.algorithm = settings.jwt.ALGORITHM

    def _create_token(
        self, type: TokenTypeEnum, claims: Mapping[str, Any], expire_minutes: int
    ) -> str:
        return JwtFactory.create_token(
            claims=claims,
            subject=type.value,
            secret_key=self.secret_key,
            algorithm=self.algorithm,
            expires_in=timedelta(minutes=expire_minutes),
        )

    def create_token(self, type: TokenTypeEnum, claims: Mapping[str, Any]) -> str:
        if type == TokenTypeEnum.ACCESS:
            return self._create_token(
                type, claims, settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        elif type == TokenTypeEnum.REFRESH:
            return self._create_token(
                type, claims, settings.jwt.REFRESH_TOKEN_EXPIRE_MINUTES
            )
        else:
            raise ValueError("Invalid token type")

    async def verify_token(self, token: str, type: TokenTypeEnum) -> dict[str, Any]:
        return await self.verifier.verify_token(
            token=token,
            expected_sub=type.value,
            secret_key=self.secret_key,
            algorithm=self.algorithm,
        )

    async def revoke_token(self, jti: str, exp: int) -> None:
        await self.blacklist.revoke(jti=jti, exp=exp)
