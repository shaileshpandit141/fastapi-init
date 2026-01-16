from typing import Annotated

from fastapi import Depends

from core.db.deps import AsyncSessionDep

from ..models.permission import Permission
from ..repositories.permission import PermissionRepository
from ..services.permission import PermissionService

# === Permission Service Dep ===


async def get_permission_service(session: AsyncSessionDep) -> PermissionService:
    return PermissionService(PermissionRepository(model=Permission, session=session))


PermissionServiceDep = Annotated[PermissionService, Depends(get_permission_service)]
