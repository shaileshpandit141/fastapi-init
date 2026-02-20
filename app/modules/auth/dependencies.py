from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from redis.asyncio import Redis

from app.adapters.db.session import AsyncSession, get_async_session
from app.adapters.redis.client import get_async_redis

from .services.current_user import CurrentUserService

# =============================================================================
# Get Current User Service With User Request Token.
# =============================================================================


async def get_current_user_service(
    token: str = Depends(
        OAuth2PasswordBearer(
            tokenUrl="/api/v1/auth/token",
            description="Use email as the username field",
        )
    ),
    redis: Redis = Depends(get_async_redis),
    session: AsyncSession = Depends(get_async_session),
) -> CurrentUserService:
    return CurrentUserService(token=token, redis=redis, session=session)
