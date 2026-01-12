from datetime import timedelta
from typing import Any

from redis.asyncio.client import Redis

from core.settings import settings

from .blocklist import JwtBlocklist
from .constants import ACCESS_SUBJECT, REFRESH_SUBJECT
from .factory import JwtFactory
from .verifier import JwtVerifier


class JwtTokenManager:
    def __init__(self, redis: Redis) -> None:
        self.blocklist = JwtBlocklist(redis)
        self.verifier = JwtVerifier(self.blocklist)

    def create_access_token(self, *, claims: dict[str, Any]) -> str:
        return JwtFactory.create(
            claims=claims,
            subject=ACCESS_SUBJECT,
            secret_key=settings.access_token_secret_key,
            algorithm=settings.algorithm,
            expires_in=timedelta(minutes=settings.access_token_expire_minutes),
        )

    def create_refresh_token(self, *, claims: dict[str, Any]) -> str:
        return JwtFactory.create(
            claims=claims,
            subject=REFRESH_SUBJECT,
            secret_key=settings.refresh_token_secret_key,
            algorithm=settings.algorithm,
            expires_in=timedelta(minutes=settings.refresh_token_expire_minutes),
        )

    async def verify_access_token(self, *, token: str) -> dict[str, Any]:
        return await self.verifier.verify(
            token=token,
            expected_sub=ACCESS_SUBJECT,
            secret_key=settings.access_token_secret_key,
            algorithm=settings.algorithm,
        )

    async def verify_refresh_token(self, *, token: str) -> dict[str, Any]:
        return await self.verifier.verify(
            token=token,
            expected_sub=REFRESH_SUBJECT,
            secret_key=settings.refresh_token_secret_key,
            algorithm=settings.algorithm,
        )

    async def revoke_token(self, *, jti: str, exp: int) -> None:
        await self.blocklist.revoke(jti=jti, exp=exp)
