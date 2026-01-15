from typing import Annotated

from fastapi import Depends

from core.db.deps import AsyncSessionDep

from .models import Permission, Role
from .repository import PermissionRepository, RoleRepository
from .service import PermissionService, RoleService


async def get_role_service(session: AsyncSessionDep) -> RoleService:
    return RoleService(RoleRepository(model=Role, session=session))


async def get_permission_service(session: AsyncSessionDep) -> PermissionService:
    return PermissionService(PermissionRepository(model=Permission, session=session))


RoleServiceDep = Annotated[RoleService, Depends(get_role_service)]
PermissionServiceDep = Annotated[PermissionService, Depends(get_permission_service)]
