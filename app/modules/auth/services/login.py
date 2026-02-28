from typing import Any, Awaitable, Callable, Mapping

from redis.asyncio.client import Redis
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.adapters.db.models.user import User
from app.adapters.jwt.exceptions import InvalidTokenError, JwtError
from app.adapters.jwt.manager import JwtTokenManager, TokenTypeEnum
from app.adapters.security.hashing import Argon2Hasher
from app.modules.auth.exceptions import UserNotFoundError

from ..policies.login import LoginPolicy

type VerifyFn = Callable[..., Awaitable[Mapping[str, Any]]]


class LoginService:
    def __init__(
        self,
        redis: Redis,
        session: AsyncSession,
        policy: LoginPolicy,
        hasher: Argon2Hasher,
        jwt_manager: JwtTokenManager,
    ) -> None:
        self.session = session
        self.redis = redis
        self.policy = policy
        self.hasher = hasher
        self.jwt_manager = jwt_manager

    async def login(self, email: str, password: str) -> dict[str, str]:

        # Check if user exists.
        stmt = select(User).where(User.email == email)
        user = (await self.session.exec(stmt)).one_or_none()
        if user is None:
            raise UserNotFoundError("User not found.")

        # Check if password is correct.
        if not self.hasher.verify(
            value=password,
            hashed=user.password_hash,
        ):
            raise UserNotFoundError("Invalid email or password.")

        # Enforce login policy.
        self.policy.enforce_can_login(user)

        return {
            "access_token": self.jwt_manager.create_token(
                TokenTypeEnum.ACCESS, {"id": str(user.id)}
            ),
            "refresh_token": self.jwt_manager.create_token(
                TokenTypeEnum.REFRESH, {"id": str(user.id)}
            ),
            "token_type": "Bearer",
        }

    async def refresh_token(self, refresh_token: str) -> dict[str, str]:
        try:
            claims = await self.jwt_manager.verify_token(
                TokenTypeEnum.REFRESH, refresh_token
            )
        except JwtError:
            raise InvalidTokenError("Invalid or expired refresh token.")

        return {
            "access_token": self.jwt_manager.create_token(
                TokenTypeEnum.ACCESS, {"id": claims["id"]}
            ),
            "refresh_token": refresh_token,
            "token_type": "Bearer",
        }

    async def revoke_token(
        self, access_token: str, refresh_token: str
    ) -> dict[str, str]:
        async def _revoke_if_valid(
            verify_fn: VerifyFn, token_type: TokenTypeEnum, token: str
        ) -> None:
            try:
                claims = await verify_fn(token_type, token)
                await self.jwt_manager.revoke_token(claims["jti"], claims["exp"])
            except JwtError:
                pass

        # Revoke access token if valid.
        await _revoke_if_valid(
            self.jwt_manager.verify_token,
            TokenTypeEnum.ACCESS,
            access_token,
        )

        # Revoke refresh token if valid.
        await _revoke_if_valid(
            self.jwt_manager.verify_token,
            TokenTypeEnum.REFRESH,
            refresh_token,
        )

        # Return success response dict.
        return {"detail": "Token revoke successful."}
