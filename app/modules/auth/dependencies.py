from fastapi import Depends
from redis.asyncio import Redis

from app.adapters.db.session import AsyncSession, get_async_session
from app.adapters.jwt.manager import JwtTokenManager
from app.adapters.redis.client import get_async_redis
from app.adapters.security.providers import get_hasher

from .policies.login import LoginPolicy
from .services.login import JwtTokenService, LoginService


async def get_login_service(
    redis: Redis = Depends(get_async_redis),
    session: AsyncSession = Depends(get_async_session),
) -> LoginService:
    return LoginService(
        redis=redis,
        session=session,
        policy=LoginPolicy(),
        hasher=get_hasher(),
        jwt_manager=JwtTokenManager(redis),
    )


# =============================================================================
# Get Jwt Token Service.
# =============================================================================


async def get_jwt_token_service(
    redis: Redis = Depends(get_async_redis),
    session: AsyncSession = Depends(get_async_session),
) -> JwtTokenService:
    return JwtTokenService(redis=redis, session=session)
