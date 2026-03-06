from redis.asyncio.client import Redis
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.adapters.db.models.user import User
from app.adapters.jwt.manager import TokenTypeEnum
from app.adapters.jwt.providers import get_jwt_token_manager
from app.adapters.security.providers import get_hasher
from app.core.exceptions.http import PermissionDeniedError
from app.modules.auth.exceptions import UserNotFoundError
from app.shared.enums.user import UserStatusEnum

from ..commands.login import LoginCommand


class LoginHandler:
    def __init__(self, redis: Redis, session: AsyncSession) -> None:
        self.redis = redis
        self.session = session
        self.hasher = get_hasher()
        self.jwt_manager = get_jwt_token_manager(redis)

    async def __call__(self, command: LoginCommand) -> dict[str, str]:
        # Check if user exists.
        stmt = select(User).where(User.email == command.email)
        user = (await self.session.exec(stmt)).one_or_none()
        if user is None:
            raise UserNotFoundError("User not found.")

        # Check if password is correct.
        if not self.hasher.verify(
            value=command.password,
            hashed=user.password_hash,
        ):
            raise UserNotFoundError("Invalid email or password.")

        if not user.is_superadmin():
            if user.status is not UserStatusEnum.ACTIVE:
                raise PermissionDeniedError("User is not active")

            if not user.is_email_verified:
                raise PermissionDeniedError("Email is not verified")

        # Return jwt tokens.
        return {
            "access_token": self.jwt_manager.create_token(
                TokenTypeEnum.ACCESS, {"id": str(user.id)}
            ),
            "refresh_token": self.jwt_manager.create_token(
                TokenTypeEnum.REFRESH, {"id": str(user.id)}
            ),
            "token_type": "Bearer",
        }
