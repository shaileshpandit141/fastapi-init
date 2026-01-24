from typing import Annotated

from fastapi import Depends

from core.db.depends import AsyncSessionDep
from domain.authorization.depends import authorize
from domain.user.models import User

from .services import UserRoleService, UserService

# === Service dependencies ===


async def get_user_service(session: AsyncSessionDep) -> UserService:
    return UserService(session=session)


async def get_user_role_service(session: AsyncSessionDep) -> UserRoleService:
    return UserRoleService(session=session)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
UserRoleServiceDep = Annotated[UserRoleService, Depends(get_user_role_service)]
CurrentUserDep = Annotated[User, Depends(authorize())]
