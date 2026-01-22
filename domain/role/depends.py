from typing import Annotated

from fastapi import Depends

from core.db.depends.async_session import AsyncSessionDep

from .services import RolePermissionService, RoleService

# === Role Service Dep ===


async def get_role_service(session: AsyncSessionDep) -> RoleService:
    return RoleService(session=session)


RoleServiceDep = Annotated[RoleService, Depends(get_role_service)]


# === Role Permission Service Dep ===


async def get_role_permission_service(
    session: AsyncSessionDep,
) -> RolePermissionService:
    return RolePermissionService(session=session)


RolePermissionServiceDep = Annotated[
    RolePermissionService, Depends(get_role_permission_service)
]
