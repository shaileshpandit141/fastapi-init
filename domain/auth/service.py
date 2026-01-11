from typing import Any, Awaitable, Callable, Mapping

from fastapi import HTTPException, status
from sqlmodel import select

from core.db.deps import AsyncSessionDep
from core.repository.exceptions import ConflictError
from core.security.jwt.exceptions import JWTError
from core.security.password import hash_password, verify_password
from domain.message.schemas import MessageRead
from domain.token.schemas import TokenRead, TokenRefresh, TokenRevoked
from domain.token.service import JwtTokenService
from domain.user.deps import UserRepositoryDep
from domain.user.models import User, UserStatus
from domain.user.schemas import UserCreate
from infrastructure.cache.redis import RedisDep

VerifyFn = Callable[..., Awaitable[Mapping[str, Any]]]


class AuthService:
    def __init__(self, *, token: JwtTokenService) -> None:
        self.token = token

    async def signup(
        self, *, user_in: UserCreate, user_repo: UserRepositoryDep
    ) -> User:
        try:
            user = await user_repo.create(
                data=user_in,
                include={"email"},
                extra={"password_hash": hash_password(user_in.password)},
            )
        except ConflictError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        return user

    async def signin(
        self, *, form_in: UserCreate, session: AsyncSessionDep
    ) -> TokenRead:

        stmt = select(User).where(User.email == form_in.email)
        user = (await session.exec(stmt)).one_or_none()

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

        if not verify_password(form_in.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email password",
            )

        return TokenRead(
            access_token=self.token.create_access_token(claims={"id": user.id}),
            refresh_token=self.token.create_refresh_token(claims={"id": user.id}),
            token_type="bearer",
        )

    async def refresh_access_token(
        self, *, token_in: TokenRefresh, redis: RedisDep
    ) -> TokenRead:
        try:
            claims = await self.token.verify_refresh_token(token=token_in.refresh_token)
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expire refresh token",
            )

        return TokenRead(
            access_token=self.token.create_access_token(claims={"id": claims["id"]}),
            refresh_token=token_in.refresh_token,
            token_type="bearer",
        )

    async def signout(self, *, token_in: TokenRevoked, redis: RedisDep) -> MessageRead:
        async def _revoke_if_valid(verify_fn: VerifyFn, token: str) -> None:
            try:
                claims = await verify_fn(redis=redis, token=token)
                await self.token.revoke_token(jti=claims["jti"], exp=claims["exp"])
            except JWTError:
                pass

        await _revoke_if_valid(self.token.verify_access_token, token_in.access_token)
        await _revoke_if_valid(self.token.verify_refresh_token, token_in.refresh_token)

        return MessageRead(detail="Sign out successful")
