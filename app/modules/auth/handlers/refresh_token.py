from redis.asyncio.client import Redis
from sqlmodel.ext.asyncio.session import AsyncSession
from app.adapters.jwt.manager import TokenTypeEnum
from app.adapters.jwt.providers import get_jwt_token_manager
from app.core.exceptions.domain import DomainError
from app.adapters.jwt.exceptions import InvalidTokenError, JwtError
from ..commands.refresh_token import RefreshTokenCommand

# =============================================================================
# User not found error.
# =============================================================================


class UserNotFoundError(DomainError):
    pass


# =============================================================================
# Refresh token handler.
# =============================================================================


class RefreshTokenHandler:
    def __init__(self, redis: Redis, session: AsyncSession) -> None:
        self.redis = redis
        self.session = session
        self.jwt_manager = get_jwt_token_manager(redis)

    async def __call__(self, command: RefreshTokenCommand) -> dict[str, str]:
        try:
            claims = await self.jwt_manager.verify_token(
                command.refresh_token, TokenTypeEnum.REFRESH
            )
        except JwtError:
            raise InvalidTokenError("Invalid or expired refresh token.")

        return {
            "access_token": self.jwt_manager.create_token(
                TokenTypeEnum.ACCESS, {"id": claims["id"]}
            ),
            "refresh_token": command.refresh_token,
            "token_type": "Bearer",
        }
