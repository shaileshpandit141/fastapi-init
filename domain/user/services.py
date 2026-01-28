# pyright: reportArgumentType=false

from typing import Sequence

from sqlmodel.ext.asyncio.session import AsyncSession

from core.exceptions import AlreadyExistsException, NotFoundException
from core.repositories.exceptions import EntityConflictException
from core.security.password.hasher import PasswordHasher

from .constants import UserStatus
from .models import User, UserRole
from .repositories import UserRepository, UserRoleRepository
from .schemas import UserCreate, UserRoleCreate, UserRoleUpdate, UserUpdate

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
                values={
                    "password_hash": password_hash,
                    "status": UserStatus.INACTIVE,
                },
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
