# pyright: reportArgumentType=false

from typing import Sequence

from core.db.imports import AsyncSession
from core.exceptions import AlreadyExistsException, NotFoundException
from core.repository.exceptions import EntityConflictException
from core.security.password.hasher import PasswordHasher

from ..models.user import User, UserStatus
from ..repositories.user import UserRepository
from ..schemas.user import UserCreate, UserUpdate

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
