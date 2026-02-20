from uuid import UUID

from redis.asyncio.client import Redis
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.adapters.db.models.user import User
from app.adapters.security.jwt.exceptions import JwtError
from app.adapters.security.jwt.manager import JwtTokenManager
from app.core.exceptions import AccessDeniedError, UnauthorizedError

from ..policies.current_user import CURRENT_USER_POLICY_MAP

# =============================================================================
# Currnet User Service.
# =============================================================================


class CurrentUserService:
    def __init__(self, token: str, redis: Redis, session: AsyncSession) -> None:
        self.token = token
        self.redis = redis
        self.session = session

    async def get_current_user(self) -> User:
        jwt_token_manager = JwtTokenManager(self.redis)

        try:
            claims = await jwt_token_manager.verify_access_token(self.token)
        except JwtError:
            raise UnauthorizedError(detail="Invalid or expired access token.")

        user = (
            await self.session.exec(
                select(User).where(
                    User.id == UUID(claims["id"]),
                )
            )
        ).one_or_none()

        if user is None:
            raise UnauthorizedError(detail="Invalid access token.")

        return user

    async def get_active_user(self) -> User:
        user = await self.get_current_user()

        try:
            state = CURRENT_USER_POLICY_MAP[user.status]
        except KeyError:
            raise AccessDeniedError("Invalid account status.")

        state.ensure_access(user)
        return user
