from typing import Sequence

from fastapi import HTTPException, status

from core.repository.exceptions import ConflictError, NotFoundError
from core.security.password.hasher import PasswordHasher
from domain.user.models import User, UserStatus
from domain.user.repository import UserRepository
from domain.user.schemas import UserCreate, UserUpdate


class UserService:
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

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
