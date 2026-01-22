from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from core.db.depends.async_session import AsyncSessionDep
from infrastructure.cache.depends.redis import RedisDep

from .services import JwtTokenService

# === Jwt Token Service Dep ===


async def get_jwt_token_service(
    session: AsyncSessionDep, redis: RedisDep
) -> JwtTokenService:
    return JwtTokenService(session=session, redis=redis)


JwtTokenServiceDep = Annotated[JwtTokenService, Depends(get_jwt_token_service)]


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
