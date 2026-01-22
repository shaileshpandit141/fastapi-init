from typing import Sequence

from fastapi import APIRouter

from core.response.swagger import ADMIN_READ
from domain.rbac.depends.require_access import AdminUserDep
from domain.rbac.depends.role import RoleServiceDep
from domain.rbac.models.role import Role
from domain.rbac.schemas.role import RoleRead

router = APIRouter(prefix="/roles", tags=["Role Endpoints"])


# === Roles specific endpoints ===


@router.get(
    path="/",
    summary="List Roles",
    description="List all roles with pagination. Only accessible by admin users.",
    response_model=list[RoleRead],
    responses=ADMIN_READ,
)
async def list_role(
    user: AdminUserDep, role_service: RoleServiceDep, limit: int = 20, offset: int = 0
) -> Sequence[Role]:
    return await role_service.list_roles(limit=limit, offset=offset)
