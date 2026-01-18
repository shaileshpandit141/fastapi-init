from typing import Annotated

from fastapi import Depends

from core.db.deps import AsyncSessionDep
from domain.auth.depends import Oauth2SchemeDep
from infrastructure.cache.redis import RedisDep

from ..services.current_user import CurrentUserService

# === Current User Service Dep ===


async def get_current_user_service(
    token: Oauth2SchemeDep, redis: RedisDep, session: AsyncSessionDep
) -> CurrentUserService:
    return CurrentUserService(token=token, redis=redis, session=session)


CurrentUserServiceDep = Annotated[CurrentUserService, Depends(get_current_user_service)]
