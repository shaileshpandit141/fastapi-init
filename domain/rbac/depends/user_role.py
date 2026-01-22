from typing import Annotated

from fastapi import Depends

from core.db.depends.async_session import AsyncSessionDep

from ..services.user_role import UserRoleService

# === User Role Service Dep ===


async def get_user_role_service(session: AsyncSessionDep) -> UserRoleService:
    return UserRoleService(session=session)


UserRoleServiceDep = Annotated[UserRoleService, Depends(get_user_role_service)]
