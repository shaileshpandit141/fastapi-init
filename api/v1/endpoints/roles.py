from typing import Sequence

from fastapi import APIRouter, status

from core.response.swagger import ADMIN_READ, ADMIN_WRITE, DELETE_RECORD
from domain.role.depends import RoleServiceDep
from domain.role.models import Role
from domain.role.policies import RolePolicy
from domain.role.schemas import RoleCreate, RoleRead, RoleUpdate

router = APIRouter(prefix="/roles", tags=["Role Endpoints"])


# === Roles specific endpoints ===


@router.post(
    path="/",
    summary="Create Role",
    description="Create a new role. Only accessible by admin users.",
    response_model=RoleRead,
    responses=ADMIN_WRITE,
)
async def create_role(
    user: RolePolicy.Admin, service: RoleServiceDep, role_in: RoleCreate
) -> Role:
    return await service.create_role(role_in=role_in)


@router.get(
    path="/",
    summary="List Roles",
    description="List all roles with pagination. Only accessible by admin users.",
    response_model=list[RoleRead],
    responses=ADMIN_READ,
)
async def list_roles(
    user: RolePolicy.Admin,
    service: RoleServiceDep,
    limit: int = 20,
    offset: int = 0,
) -> Sequence[Role]:
    return await service.list_roles(limit=limit, offset=offset)


@router.get(
    path="/{role_id}",
    summary="Get Role",
    description="Retrieve a specific role by its ID. Only accessible by admin users.",
    response_model=RoleRead,
    responses=ADMIN_READ,
)
async def get_role(
    user: RolePolicy.Admin,
    service: RoleServiceDep,
    role_id: int,
) -> Role:
    return await service.get_role(role_id=role_id)


@router.patch(
    path="/{role_id}",
    summary="Update a Role",
    description="Update a specific role by its ID. Only accessible by admin users.",
    response_model=RoleRead,
    responses=ADMIN_WRITE,
)
async def update_role(
    user: RolePolicy.Admin,
    service: RoleServiceDep,
    role_id: int,
    role_in: RoleUpdate,
) -> Role:
    return await service.update_role(role_id=role_id, role_in=role_in)


@router.patch(
    path="/{role_id}",
    summary="Delete a Role",
    description="Delete a specific role by its ID. Only accessible by admin users.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=DELETE_RECORD,
)
async def delete_role(
    user: RolePolicy.Admin,
    service: RoleServiceDep,
    role_id: int,
) -> None:
    await service.delete_role(role_id=role_id)
