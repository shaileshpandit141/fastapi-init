# pyright: reportArgumentType=false

from typing import Sequence

from fastapi import HTTPException, status

from core.db import AsyncSession
from core.repository.exceptions import ConflictError, NotFoundError
from core.security.password.hasher import PasswordHasher

from ..models.user import User, UserStatus
from ..repositories.user import UserRepository
from ..schemas.user import UserCreate, UserUpdate

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
