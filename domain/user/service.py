# pyright: reportArgumentType=false

from typing import Sequence

from fastapi import HTTPException, status
from redis.asyncio.client import Redis
from sqlalchemy.orm import selectinload
from sqlmodel import select

from core.db import AsyncSession
from core.repository.exceptions import ConflictError, NotFoundError
from core.security.jwt.exceptions import JwtError
from core.security.jwt.manager import JwtTokenManager
from core.security.password.hasher import PasswordHasher
from domain.rbac.models.role import Role
from domain.rbac.models.role_permission import RolePermission
from domain.rbac.models.user_role import UserRole
from domain.user.models import User, UserStatus
from domain.user.repository import UserRepository
from domain.user.schemas import UserCreate, UserUpdate

# === Current User Service ===


class CurrentUserService:
    def __init__(self, token: str, redis: Redis, session: AsyncSession) -> None:
        self.token = token
        self.redis = redis
        self.session = session

    async def get_current_user(self) -> User:
        jwt_token_manager = JwtTokenManager(self.redis)

        try:
            claims = await jwt_token_manager.verify_access_token(self.token)
        except (JwtError, KeyError, ValueError):
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired access token",
                headers={"WWW-Authenticate": "Bearer"},
            )

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
            raise HTTPException(
                status_code=401,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user

    async def get_active_user(self) -> User:
        user = await self.get_current_user()

        if user.status != UserStatus.ACTIVE:
            raise HTTPException(
                status_code=403,
                detail="Inactive user",
            )

        return user


# === User Service ===


class UserService:
    def __init__(self, model: type[User], session: AsyncSession) -> None:
        self.user_repo = UserRepository(model=model, session=session)

    async def create_user(self, user_in: UserCreate) -> User:

        hasher = PasswordHasher()
        password_hash = hasher.hash_password(user_in.password)

        try:
            user = await self.user_repo.create(
                data=user_in,
                include={"email"},
                extra={
                    "password_hash": password_hash,
                    "status": UserStatus.ACTIVE,
                },
            )
        except ConflictError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        return user

    async def get_user(self, user_id: int) -> User:
        try:
            user = await self.user_repo.get_or_raise(id=user_id)
        except NotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User does not exist",
            )

        return user

    async def list_user(self, limit: int = 20, offset: int = 0) -> Sequence[User]:
        users = await self.user_repo.list(
            limit=limit,
            offset=offset,
        )

        return users

    async def update_user(self, user_id: int, user_in: UserUpdate) -> User:
        db_user = await self.get_user(user_id)

        user = await self.user_repo.update(
            obj=db_user,
            data=user_in,
        )

        return user

    async def delete_user(self, user_id: int) -> None:
        try:
            await self.user_repo.delete_by_id(id=user_id)
        except NotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
            )
