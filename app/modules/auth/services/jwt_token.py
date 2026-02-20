from typing import Any, Awaitable, Callable, Mapping

from redis.asyncio.client import Redis
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.adapters.db.models.user import User
from app.adapters.security.jwt.exceptions import JwtError
from app.adapters.security.jwt.manager import JwtTokenManager
from app.adapters.security.password.hasher import PasswordHasher
from app.core.exceptions import AccessDeniedError, BadRequestError
from app.shared.enums.user import UserStatus
from app.shared.response.schemas import DetailResponse

type VerifyFn = Callable[..., Awaitable[Mapping[str, Any]]]


# =============================================================================
# Jwt Token Service.
# =============================================================================


class JwtTokenService:
    def __init__(self, redis: Redis, session: AsyncSession) -> None:
        self._session = session
        self._jwt = JwtTokenManager(redis=redis)
        self._hasher = PasswordHasher()

    async def create_jwt_token(self, email: str, password: str) -> dict[str, str]:

        stmt = select(User).where(User.email == email)
        user = (await self._session.exec(stmt)).one_or_none()

        if not user:
            raise BadRequestError(detail="User not found.")

        if user.status == UserStatus.INACTIVE:
            raise AccessDeniedError(detail="Inactive user.")

        if not user.is_email_verified:
            raise AccessDeniedError(
                detail="Please verify your email to continue.",
            )

        if not self._hasher.verify_password(
            plain_password=password,
            hashed_password=user.password_hash,
        ):
            raise BadRequestError(detail="Incorrect email password.")

        return {
            "access_token": self._jwt.create_access_token(claims={"id": str(user.id)}),
            "refresh_token": self._jwt.create_refresh_token(
                claims={"id": str(user.id)}
            ),
            "token_type": "Bearer",
        }

    async def refresh_access_token(self, refresh_token: str) -> dict[str, str]:
        try:
            claims = await self._jwt.verify_refresh_token(token=refresh_token)
        except JwtError:
            raise BadRequestError(detail="Invalid or expire refresh token.")

        return {
            "access_token": self._jwt.create_access_token(claims={"id": claims["id"]}),
            "refresh_token": refresh_token,
            "token_type": "Bearer",
        }

    async def revoke_token(
        self, access_token: str, refresh_token: str
    ) -> DetailResponse:
        async def _revoke_if_valid(verify_fn: VerifyFn, token: str) -> None:
            try:
                claims = await verify_fn(token=token)
                await self._jwt.revoke_token(jti=claims["jti"], exp=claims["exp"])
            except JwtError:
                pass

        await _revoke_if_valid(
            self._jwt.verify_access_token,
            access_token,
        )
        await _revoke_if_valid(
            self._jwt.verify_refresh_token,
            refresh_token,
        )

        return DetailResponse(detail="Token revoke successful.")
