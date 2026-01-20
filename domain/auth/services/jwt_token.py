from typing import Any, Awaitable, Callable, Mapping

from redis.asyncio.client import Redis
from sqlmodel import select

from core.db.imports import AsyncSession
from core.exceptions import AccessDeniedException, BadRequestException
from core.response.schemas import DetailResponse
from core.security.jwt import JwtTokenManager
from core.security.jwt.exceptions import JwtException
from core.security.password import PasswordHasher
from domain.user.models.user import User, UserStatus

from ..schemas.jwt_token import (
    JwtTokenCreate,
    JwtTokenRead,
    JwtTokenRefresh,
    JwtTokenRevoked,
)

VerifyFn = Callable[..., Awaitable[Mapping[str, Any]]]

# === Jwt Token Service ===


class JwtTokenService:
    def __init__(self, *, session: AsyncSession, redis: Redis) -> None:
        self._session = session
        self._jwt_token_manager = JwtTokenManager(redis=redis)
        self._password_hasher = PasswordHasher()

    async def create_jwt_token(self, *, form_in: JwtTokenCreate) -> JwtTokenRead:

        stmt = select(User).where(User.email == form_in.email)
        user = (await self._session.exec(stmt)).one_or_none()

        if not user:
            raise BadRequestException(message="User not found")

        if user.status == UserStatus.INACTIVE:
            raise AccessDeniedException(message="User is inactive")

        if not self._password_hasher.verify_password(
            plain_password=form_in.password, hashed_password=user.password_hash
        ):
            raise BadRequestException(message="Incorrect email password")

        return JwtTokenRead(
            access_token=self._jwt_token_manager.create_access_token(
                claims={"id": user.id}
            ),
            refresh_token=self._jwt_token_manager.create_refresh_token(
                claims={"id": user.id}
            ),
            token_type="bearer",
        )

    async def refresh_access_token(self, *, token_in: JwtTokenRefresh) -> JwtTokenRead:
        try:
            claims = await self._jwt_token_manager.verify_refresh_token(
                token=token_in.refresh_token
            )
        except JwtException:
            raise BadRequestException(message="Invalid or expire refresh token")

        return JwtTokenRead(
            access_token=self._jwt_token_manager.create_access_token(
                claims={"id": claims["id"]}
            ),
            refresh_token=token_in.refresh_token,
            token_type="bearer",
        )

    async def revoke_token(self, *, token_in: JwtTokenRevoked) -> DetailResponse:
        async def _revoke_if_valid(verify_fn: VerifyFn, token: str) -> None:
            try:
                claims = await verify_fn(token=token)
                await self._jwt_token_manager.revoke_token(
                    jti=claims["jti"], exp=claims["exp"]
                )
            except JwtException:
                pass

        await _revoke_if_valid(
            self._jwt_token_manager.verify_access_token,
            token_in.access_token,
        )
        await _revoke_if_valid(
            self._jwt_token_manager.verify_refresh_token,
            token_in.refresh_token,
        )

        return DetailResponse(detail="Token revoke successful")
