# pyright: reportArgumentType=false

from typing import Any, Awaitable, Callable, Mapping

from redis.asyncio.client import Redis
from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.exceptions import AccessDeniedError, BadRequestError
from core.exceptions.http_exception import UnauthorizedError
from core.response.schemas import DetailResponse
from core.security.jwt import JwtTokenManager
from core.security.jwt.exceptions import JwtError
from core.security.password import PasswordHasher
from domain.role.models import Role, RolePermission
from domain.user.constants import UserStatus
from domain.user.models import User, UserRole

from .schemas import JwtTokenCreate, JwtTokenRead, JwtTokenRefresh, JwtTokenRevoked

VerifyFn = Callable[..., Awaitable[Mapping[str, Any]]]


# === Current User Service ===


class CurrentUserService:
    def __init__(self, token: str, redis: Redis, session: AsyncSession) -> None:
        self.token = token
        self.redis = redis
        self.session = session

    async def get_current_user(self) -> User:
        jwt_token_manager = JwtTokenManager(self.redis)
        # cache = CurrentUserCache(self.redis)

        try:
            claims = await jwt_token_manager.verify_access_token(self.token)
        except JwtError:
            raise UnauthorizedError(detail="Invalid or expired access token.")

        # cache_user = await cache.get(id=claims["id"])  # type: ignore # noqa: F841

        # print("==========================")
        # print("Cache User: ", cache_user)

        # if cache_user:
        #     return cache_user

        stmt = (
            select(User)
            .where(User.id == claims["id"])
            .options(
                selectinload(User.roles)
                .selectinload(UserRole.role)
                .selectinload(Role.permissions)
                .selectinload(RolePermission.permission)
            )
        )

        user = (await self.session.exec(stmt)).one_or_none()

        if user is None:
            raise UnauthorizedError(detail="Invalid access token.")

        # await cache.set(id=user.id, instance=user)

        return user

    async def get_active_user(self) -> User:
        user = await self.get_current_user()

        if user.status != UserStatus.ACTIVE:
            raise AccessDeniedError(detail="Inactive user.")

        if not user.is_email_verified:
            raise AccessDeniedError(
                detail="Please verify your email to continue.",
            )

        return user


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
            raise BadRequestError(detail="User not found.")

        if user.status == UserStatus.INACTIVE:
            raise AccessDeniedError(detail="Inactive user.")

        if not user.is_email_verified:
            raise AccessDeniedError(
                detail="Please verify your email to continue.",
            )

        if not self._password_hasher.verify_password(
            plain_password=form_in.password, hashed_password=user.password_hash
        ):
            raise BadRequestError(detail="Incorrect email password.")

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
        except JwtError:
            raise BadRequestError(detail="Invalid or expire refresh token.")

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
            except JwtError:
                pass

        await _revoke_if_valid(
            self._jwt_token_manager.verify_access_token,
            token_in.access_token,
        )
        await _revoke_if_valid(
            self._jwt_token_manager.verify_refresh_token,
            token_in.refresh_token,
        )

        return DetailResponse(detail="Token revoke successful.")
