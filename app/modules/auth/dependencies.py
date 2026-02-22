from fastapi import Depends
from redis.asyncio import Redis

from app.adapters.db.session import AsyncSession, get_async_session
from app.adapters.redis.client import get_async_redis

from .services.login import JwtTokenService

# =============================================================================
# Get Jwt Token Service.
# =============================================================================


async def get_jwt_token_service(
    redis: Redis = Depends(get_async_redis),
    session: AsyncSession = Depends(get_async_session),
) -> JwtTokenService:
    return JwtTokenService(redis=redis, session=session)
