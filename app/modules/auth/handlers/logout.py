from typing import Any, Awaitable, Callable, Mapping

from redis.asyncio.client import Redis
from sqlmodel.ext.asyncio.session import AsyncSession

from app.adapters.jwt.exceptions import JwtError
from app.adapters.jwt.manager import TokenTypeEnum
from app.adapters.jwt.providers import get_jwt_token_manager

from ..commands.logout import LogoutCommand

type VerifyFn = Callable[..., Awaitable[Mapping[str, Any]]]


class LogoutHandler:
    def __init__(self, redis: Redis, session: AsyncSession) -> None:
        self.redis = redis
        self.session = session
        self.jwt_manager = get_jwt_token_manager(redis)

    async def _revoke_if_valid(self, token: str, type: TokenTypeEnum) -> None:
        try:
            claims = await self.jwt_manager.verify_token(token, type)
            await self.jwt_manager.revoke_token(claims["jti"], claims["exp"])
        except JwtError:
            pass

    async def __call__(self, command: LogoutCommand) -> dict[str, str]:
        # Revoke access token if valid.
        await self._revoke_if_valid(command.access_token, TokenTypeEnum.ACCESS)

        # Revoke refresh token if valid.
        await self._revoke_if_valid(command.refresh_token, TokenTypeEnum.REFRESH)

        # Return success response dict.
        return {"detail": "Token revoke successful."}
