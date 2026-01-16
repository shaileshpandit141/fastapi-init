from typing import Annotated

from fastapi import Depends

from core.db.deps import AsyncSessionDep

from ..models.role import Role
from ..repositories.role import RoleRepository
from ..services.role import RoleService

# === Role Service Dep ===


async def get_role_service(session: AsyncSessionDep) -> RoleService:
    return RoleService(RoleRepository(model=Role, session=session))


RoleServiceDep = Annotated[RoleService, Depends(get_role_service)]
