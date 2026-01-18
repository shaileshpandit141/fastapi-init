from typing import Annotated

from fastapi import Depends

from core.db.depends import AsyncSessionDep

from ..models.role_permission import RolePermission
from ..services.role_permission import RolePermissionService

# === Role Permission Service Dep ===


async def get_role_permission_service(
    session: AsyncSessionDep,
) -> RolePermissionService:
    return RolePermissionService(model=RolePermission, session=session)


RolePermissionServiceDep = Annotated[
    RolePermissionService, Depends(get_role_permission_service)
]
