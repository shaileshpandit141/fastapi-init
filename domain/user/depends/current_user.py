from typing import Annotated

from fastapi import Depends

from core.db.depends.async_session import AsyncSessionDep
from domain.auth.depends.oauth2 import OAuth2PasswordBearerDep
from infrastructure.cache.depends.redis import RedisDep

from ..services.current_user import CurrentUserService

# === Current User Service Dep ===


async def get_current_user_service(
    token: OAuth2PasswordBearerDep, redis: RedisDep, session: AsyncSessionDep
) -> CurrentUserService:
    return CurrentUserService(token=token, redis=redis, session=session)


CurrentUserServiceDep = Annotated[CurrentUserService, Depends(get_current_user_service)]
