from logging import getLogger
from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from core.security.password import hash_password
from models.user import User, UserStatus
from schemas.user import UserCreate
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
        stmt = select(User).where(User.status == UserStatus.ACTIVE)
        user = (await self.session.exec(stmt)).one_or_none()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return user
