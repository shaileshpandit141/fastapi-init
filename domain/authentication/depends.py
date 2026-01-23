from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from core.db.depends.async_session import AsyncSessionDep
from infrastructure.cache.depends.redis import RedisDep

from .services import CurrentUserService, JwtTokenService

# === OAuth2 Deps ===


async def get_oauth2_password_bearer(
    token: str = Depends(
        OAuth2PasswordBearer(
            tokenUrl="/api/v1/auth/token",
            description="Use email as the username field",
        )
    ),
) -> str:
    return token


OAuth2PasswordBearerDep = Annotated[str, Depends(get_oauth2_password_bearer)]
OAuth2PasswordRequestFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]


# === Current User Service Dep ===


async def get_authenticated_user_service(
    token: OAuth2PasswordBearerDep, redis: RedisDep, session: AsyncSessionDep
) -> CurrentUserService:
    return CurrentUserService(token=token, redis=redis, session=session)


CurrentUserServiceDep = Annotated[
    CurrentUserService, Depends(get_authenticated_user_service)
]


# === Jwt Token Service Dep ===


async def get_jwt_token_service(
    session: AsyncSessionDep, redis: RedisDep
) -> JwtTokenService:
    return JwtTokenService(session=session, redis=redis)


JwtTokenServiceDep = Annotated[JwtTokenService, Depends(get_jwt_token_service)]
