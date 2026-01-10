# pyright: reportCallIssue=false

from logging import getLogger
from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from core.security.password import hash_password
from models.user import User, UserStatus
from schemas.user import UserCreate, UserUpdate
from services.base import AsyncSessionService

logger = getLogger(__name__)


class UserService(AsyncSessionService):
    """Service to mange user table"""

    async def create_user(self, *, data: UserCreate) -> User:
        """Create a new user with email and password"""
        user = User(
            email=data.email,
            password_hash=hash_password(data.password),
            status=UserStatus.ACTIVE,
        )

        self.session.add(user)

        try:
            await self.session.commit()
            await self.session.refresh(user)
        except IntegrityError:
            logger.debug("User creation failed: ", exc_info=True)
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )

        return user

    async def list_users(self, *, limit: int = 8, offset: int = 0) -> Sequence[User]:
        """Sequence of user records"""
        stmt = select(User).limit(limit).offset(offset)
        result = await self.session.exec(stmt)
        return result.all()

    async def get_user(self, *, user_id: int) -> User:
        """Get a user by ID"""
        stmt = select(User).where(User.id == user_id, User.status == UserStatus.ACTIVE)
        user = (await self.session.exec(stmt)).one_or_none()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return user

    async def update_user(self, *, user: User, data: UserUpdate) -> User:
        """Update user with provided data"""

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)

        try:
            await self.session.commit()
            await self.session.refresh(user)
        except IntegrityError as error:
            logger.warning("User update failed", exc_info=error)
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User update violates database constraints",
            )

        return user

    async def delete_user(self, *, user: User) -> None:
        """Delete user instance"""

        try:
            await self.session.delete(user)
            await self.session.commit()
        except Exception as error:
            await self.session.rollback()
            logger.warning("User delete failed", exc_info=error)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to delete user",
            )

    async def delete_user_by_id(self, *, user_id: int) -> None:
        """Deleting user by it's ID"""
        user = await self.get_user(user_id=user_id)
        await self.delete_user(user=user)
