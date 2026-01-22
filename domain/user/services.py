# pyright: reportArgumentType=false

from typing import Sequence

from redis.asyncio.client import Redis
from sqlalchemy.orm import selectinload
from sqlmodel import select

from core.db.imports import AsyncSession
from core.exceptions import (
    AccessDeniedException,
    AlreadyExistsException,
    NotFoundException,
    UnauthorizedException,
)
from core.repository.exceptions import EntityConflictException
from core.security.jwt.exceptions import JwtException
from core.security.jwt.manager import JwtTokenManager
from core.security.password.hasher import PasswordHasher
from domain.role.models import Role, RolePermission

from .models import User, UserRole, UserStatus
from .repositories import UserRepository, UserRoleRepository
from .schemas import UserCreate, UserRoleCreate, UserRoleUpdate, UserUpdate

# === Current User Service ===


class CurrentUserService:
    def __init__(self, token: str, redis: Redis, session: AsyncSession) -> None:
        self.token = token
        self.redis = redis
        self.session = session

    async def get_current_user(self) -> User:
        jwt_token_manager = JwtTokenManager(self.redis)
        # cache = CurrentUserCache(self.redis)

        try:
            claims = await jwt_token_manager.verify_access_token(self.token)
        except JwtException:
            raise UnauthorizedException(detail="Invalid or expired access token.")

        # cache_user = await cache.get(id=claims["id"])  # type: ignore # noqa: F841

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

        # await cache.set(id=user.id, instance=user)

        return user

    async def get_active_user(self) -> User:
        user = await self.get_current_user()

        if user.status != UserStatus.ACTIVE:
            raise AccessDeniedException(detail="Inactive user.")

        return user


# === User Service ===


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = UserRepository(model=User, session=session)

    async def create_user(self, user_in: UserCreate) -> User:

        hasher = PasswordHasher()
        password_hash = hasher.hash_password(user_in.password)

        try:
            user = await self.repo.create(
                data=user_in,
                values={"password_hash": password_hash, "status": UserStatus.ACTIVE},
            )
        except EntityConflictException:
            raise AlreadyExistsException(detail="Email already exists.")

        return user

    async def get_user(self, user_id: int) -> User:
        user = await self.repo.get(id=user_id)

        if not user:
            raise NotFoundException(detail="User not found.")

        return user

    async def list_user(self, limit: int = 20, offset: int = 0) -> Sequence[User]:
        return await self.repo.list(limit=limit, offset=offset, order_by=User.id)

    async def update_user(self, user_id: int, user_in: UserUpdate) -> User:
        user = await self.get_user(user_id)
        return await self.repo.update(obj=user, data=user_in)

    async def delete_user(self, user_id: int) -> None:
        user = await self.get_user(user_id)
        await self.repo.delete(obj=user)
        return None


# === User Role Service ===


class UserRoleService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = UserRoleRepository(model=UserRole, session=session)

    async def create_user_role(
        self, user_id: int, user_role_in: UserRoleCreate
    ) -> UserRole:
        try:
            user_role = await self.repo.create(
                data=user_role_in, values={"user_id": user_id}
            )
        except EntityConflictException:
            raise AlreadyExistsException(detail="User role already exists.")

        return user_role

    async def get_user_role(self, user_id: int) -> UserRole:
        role = await self.repo.get_by(user_id=user_id)

        if not role:
            raise NotFoundException(detail="User role not found.")

        return role

    async def list_user_roles(
        self, user_id: int, limit: int = 20, offset: int = 0
    ) -> Sequence[UserRole]:
        roles = await self.repo.find_by(
            conditions=[UserRole.user_id == user_id], limit=limit, offset=offset
        )
        return roles

    async def update_user_role(
        self, user_id: int, user_role_in: UserRoleUpdate
    ) -> UserRole:
        user_role = await self.get_user_role(user_id=user_id)

        user_role = await self.repo.update(obj=user_role, data=user_role_in)

        return user_role

    async def delete_user_role(self, user_id: int, role_id: int) -> None:
        role = await self.repo.get_by(user_id=user_id, role_id=role_id)

        if not role:
            raise NotFoundException(detail="Role does not exists")

        await self.repo.delete(obj=role)
