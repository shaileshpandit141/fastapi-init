from typing import Annotated

from fastapi import Depends

from core.db.deps import AsyncSessionDep
from domain.auth.depends import Oauth2SchemeDep
from domain.user.service import CurrentUserService, UserService
from infrastructure.cache.redis import RedisDep

from .models import User
from .repository import UserRepository


async def get_current_user_service(
    token: Oauth2SchemeDep, redis: RedisDep, session: AsyncSessionDep
) -> CurrentUserService:
    return CurrentUserService(token=token, redis=redis, session=session)


async def get_user_service(session: AsyncSessionDep) -> UserService:
    return UserService(UserRepository(model=User, session=session))


CurrentUserServiceDep = Annotated[CurrentUserService, Depends(get_current_user_service)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
