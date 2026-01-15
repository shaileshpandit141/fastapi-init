from typing import Annotated

from fastapi import Depends

from core.db.deps import AsyncSessionDep

from .models import Role
from .repository import RoleRepository
from .service import RoleService


async def get_role_service(session: AsyncSessionDep) -> RoleService:
    return RoleService(RoleRepository(model=Role, session=session))


RoleServiceDep = Annotated[RoleService, Depends(get_role_service)]
