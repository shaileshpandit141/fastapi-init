from typing import Annotated

from fastapi import Depends

from core.db.deps import AsyncSessionDep

from .models import Permission, Role, RolePermission
from .repository import PermissionRepository, RolePermissionRepository, RoleRepository
from .service import PermissionService, RolePermissionService, RoleService


async def get_role_service(session: AsyncSessionDep) -> RoleService:
    return RoleService(RoleRepository(model=Role, session=session))


async def get_permission_service(session: AsyncSessionDep) -> PermissionService:
    return PermissionService(PermissionRepository(model=Permission, session=session))


async def get_role_permission_service(
    session: AsyncSessionDep,
) -> RolePermissionService:
    return RolePermissionService(
        RolePermissionRepository(model=RolePermission, session=session)
    )


RoleServiceDep = Annotated[RoleService, Depends(get_role_service)]
PermissionServiceDep = Annotated[PermissionService, Depends(get_permission_service)]
RolePermissionServiceDep = Annotated[
    RolePermissionService, Depends(get_role_permission_service)
]
