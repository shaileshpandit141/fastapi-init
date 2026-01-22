from typing import Annotated

from fastapi import Depends

from core.db.depends.async_session import AsyncSessionDep

from ..services.role import RoleService

# === Role Service Dep ===


async def get_role_service(session: AsyncSessionDep) -> RoleService:
    return RoleService(session=session)


RoleServiceDep = Annotated[RoleService, Depends(get_role_service)]
