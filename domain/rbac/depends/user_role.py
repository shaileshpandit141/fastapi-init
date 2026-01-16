from typing import Annotated

from fastapi import Depends

from core.db.deps import AsyncSessionDep

from ..models.user_role import UserRole
from ..repositories.user_role import UserRoleRepository
from ..services.user_role import UserRoleService

# === User Role Service Dep ===


async def get_user_role_service(session: AsyncSessionDep) -> UserRoleService:
    return UserRoleService(UserRoleRepository(model=UserRole, session=session))


UserRoleServiceDep = Annotated[UserRoleService, Depends(get_user_role_service)]
