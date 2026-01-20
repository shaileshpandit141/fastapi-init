# pyright: reportArgumentType=false

from redis.asyncio.client import Redis
from sqlalchemy.orm import selectinload
from sqlmodel import select

from core.db.imports import AsyncSession
from core.exceptions import AccessDeniedException, UnauthorizedException
from core.security.jwt.exceptions import JwtException
from core.security.jwt.manager import JwtTokenManager
from domain.rbac.models.role import Role
from domain.rbac.models.role_permission import RolePermission
from domain.rbac.models.user_role import UserRole

from ..cache.current_user import CurrentUserCache
from ..models.user import User, UserStatus

# === Current User Service ===


class CurrentUserService:
    def __init__(self, token: str, redis: Redis, session: AsyncSession) -> None:
        self.token = token
        self.redis = redis
        self.session = session

    async def get_current_user(self) -> User:
        jwt_token_manager = JwtTokenManager(self.redis)
        cache = CurrentUserCache(self.redis)

        try:
            claims = await jwt_token_manager.verify_access_token(self.token)
        except JwtException:
            raise UnauthorizedException(detail="Invalid or expired access token.")

        cache_user = await cache.get(id=claims["id"])  # type: ignore # noqa: F841

        # print("==========================")
        # print("Cache User: ", cache_user)

        # if cache_user:
        #     return cache_user

        stmt = (
            select(User)
            .where(User.id == claims["id"])
            .options(
                selectinload(User.roles)
                .selectinload(UserRole.role)
                .selectinload(Role.permissions)
                .selectinload(RolePermission.permission)
            )
        )

        user = (await self.session.exec(stmt)).one_or_none()

        if user is None:
            raise UnauthorizedException(detail="Invalid access token.")

        await cache.set(id=user.id, instance=user)

        return user

    async def get_active_user(self) -> User:
        user = await self.get_current_user()

        if user.status != UserStatus.ACTIVE:
            raise AccessDeniedException(detail="Inactive user.")

        return user
