from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from redis.asyncio import Redis
from sqlmodel import UUID, select

from app.adapters.db.models.user import User
from app.adapters.db.session import AsyncSession, get_async_session
from app.adapters.redis.client import get_async_redis
from app.adapters.jwt.exceptions import JwtError
from app.adapters.jwt.manager import JwtTokenManager, TokenTypeEnum

# =============================================================================
# Get current user function.
# =============================================================================


async def get_current_user(
    token: str = Depends(
        OAuth2PasswordBearer(
            tokenUrl="/api/v1/auth/login",
            description="Use email as the username field",
        )
    ),
    redis: Redis = Depends(get_async_redis),
    session: AsyncSession = Depends(get_async_session),
) -> User:
    jwt_token_manager = JwtTokenManager(redis)

    try:
        claims = await jwt_token_manager.verify_token(
            token,
            TokenTypeEnum.ACCESS,
        )
    except JwtError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access token.",
        )

    user = (
        await session.exec(
            select(User).where(
                User.id == UUID(claims["id"]),
            )
        )
    ).one_or_none()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    return user
