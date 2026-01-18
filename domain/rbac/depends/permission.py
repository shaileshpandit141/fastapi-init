from typing import Annotated

from fastapi import Depends

from core.db.depends.async_session import AsyncSessionDep

from ..models.permission import Permission
from ..services.permission import PermissionService

# === Permission Service Dep ===


async def get_permission_service(session: AsyncSessionDep) -> PermissionService:
    return PermissionService(model=Permission, session=session)


PermissionServiceDep = Annotated[PermissionService, Depends(get_permission_service)]
