from typing import Annotated

from fastapi import Depends

from core.db.depends import AsyncSessionDep

from .services import RolePermissionService, RoleService

# === Service dependencies ===


async def get_role_service(session: AsyncSessionDep) -> RoleService:
    return RoleService(session=session)


async def get_role_permission_service(
    session: AsyncSessionDep,
) -> RolePermissionService:
    return RolePermissionService(session=session)


RoleServiceDep = Annotated[RoleService, Depends(get_role_service)]
RolePermissionServiceDep = Annotated[
    RolePermissionService, Depends(get_role_permission_service)
]
