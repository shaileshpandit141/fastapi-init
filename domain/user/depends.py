from typing import Annotated

from fastapi import Depends

from core.db.depends.async_session import AsyncSessionDep
from domain.authentication.depends import OAuth2PasswordBearerDep
from infrastructure.cache.depends.redis import RedisDep

from .services import CurrentUserService, UserRoleService, UserService

# === Current User Service Dep ===


async def get_current_user_service(
    token: OAuth2PasswordBearerDep, redis: RedisDep, session: AsyncSessionDep
) -> CurrentUserService:
    return CurrentUserService(token=token, redis=redis, session=session)


CurrentUserServiceDep = Annotated[CurrentUserService, Depends(get_current_user_service)]


# === User Service Dep ===


async def get_user_service(session: AsyncSessionDep) -> UserService:
    return UserService(session=session)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


# === User Role Service Dep ===


async def get_user_role_service(session: AsyncSessionDep) -> UserRoleService:
    return UserRoleService(session=session)


UserRoleServiceDep = Annotated[UserRoleService, Depends(get_user_role_service)]
