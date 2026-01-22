from typing import Annotated

from fastapi import Depends

from core.db.depends.async_session import AsyncSessionDep

from .services import PermissionService

# === Permission Service Dep ===


async def get_permission_service(session: AsyncSessionDep) -> PermissionService:
    return PermissionService(session=session)


PermissionServiceDep = Annotated[PermissionService, Depends(get_permission_service)]
