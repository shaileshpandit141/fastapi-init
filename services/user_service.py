from logging import getLogger

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

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
