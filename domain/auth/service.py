from typing import Any, Awaitable, Callable, Mapping

from fastapi import HTTPException, status
from redis.asyncio.client import Redis
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from core.db import AsyncSession
from core.security.jwt import JwtTokenManager
from core.security.jwt.exceptions import JwtError
from core.security.password import PasswordHasher
from domain.response.schemas import DetailResponse
from domain.user.models import User, UserStatus
from domain.user.schemas import UserCreate

from .schemas import JwtTokenCreate, TokenRead, TokenRefresh, TokenRevoked

VerifyFn = Callable[..., Awaitable[Mapping[str, Any]]]


class AuthService:
    def __init__(self, *, session: AsyncSession, redis: Redis) -> None:
        self._session = session
        self._jwt_token_manager = JwtTokenManager(redis=redis)
        self._password_hasher = PasswordHasher()

    async def register(self, *, user_in: UserCreate) -> User:
        try:
            user = User(
                email=user_in.email,
                password_hash=self._password_hasher.hash_password(
                    password=user_in.password
                ),
                status=UserStatus.ACTIVE,
            )  # pyright: ignore[reportCallIssue]
            self._session.add(user)
            await self._session.commit()
            await self._session.refresh(user)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        return user

    async def create_jwt_token(self, *, form_in: JwtTokenCreate) -> TokenRead:

        stmt = select(User).where(User.email == form_in.email)
        user = (await self._session.exec(stmt)).one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not found",
            )

        if user.status == UserStatus.INACTIVE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is inactive",
            )

        if not self._password_hasher.verify_password(
            plain_password=form_in.password, hashed_password=user.password_hash
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email password",
            )

        return TokenRead(
            access_token=self._jwt_token_manager.create_access_token(
                claims={"id": user.id}
            ),
            refresh_token=self._jwt_token_manager.create_refresh_token(
                claims={"id": user.id}
            ),
            token_type="bearer",
        )

    async def refresh_access_token(self, *, token_in: TokenRefresh) -> TokenRead:
        try:
            claims = await self._jwt_token_manager.verify_refresh_token(
                token=token_in.refresh_token
            )
        except JwtError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expire refresh token",
            )

        return TokenRead(
            access_token=self._jwt_token_manager.create_access_token(
                claims={"id": claims["id"]}
            ),
            refresh_token=token_in.refresh_token,
            token_type="bearer",
        )

    async def revoke_token(self, *, token_in: TokenRevoked) -> DetailResponse:
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

        return DetailResponse(detail="Token revoke successful")
