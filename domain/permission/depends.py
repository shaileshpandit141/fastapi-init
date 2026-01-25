from typing import Annotated

from fastapi import Depends

from core.db.depends import AsyncSessionDep

from .services import PermissionService

# === Service dependencies ===


async def get_permission_service(session: AsyncSessionDep) -> PermissionService:
    return PermissionService(session=session)


PermissionServiceDep = Annotated[PermissionService, Depends(get_permission_service)]
