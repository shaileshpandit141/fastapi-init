from typing import Sequence

from fastapi import APIRouter

from core.response.swagger import ADMIN_READ, ADMIN_WRITE
from domain.role.depends import RoleAccess, RoleServices
from domain.role.models import Role
from domain.role.schemas import RoleCreate, RoleRead

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
    user: RoleAccess.Admin,
    role_service: RoleServices.Role,
    limit: int = 20,
    offset: int = 0,
) -> Sequence[Role]:
    return await role_service.list_roles(limit=limit, offset=offset)


@router.post(
    path="/",
    summary="Create Role",
    description="Create a new role. Only accessible by admin users.",
    response_model=RoleRead,
    responses=ADMIN_WRITE,
)
async def create_role(
    user: RoleAccess.Admin, role_service: RoleServices.Role, role_in: RoleCreate
) -> Role:
    return await role_service.create_role(role_in=role_in)
