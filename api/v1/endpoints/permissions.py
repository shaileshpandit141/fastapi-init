from typing import Sequence

from fastapi import APIRouter, status

from core.response.swagger import ADMIN_READ, ADMIN_WRITE, DELETE_RECORD
from domain.permission.depends import PermissionServiceDep
from domain.permission.models import Permission
from domain.permission.policies import PermissionPolicy
from domain.permission.schemas import PermissionCreate, PermissionRead, PermissionUpdate

router = APIRouter(prefix="/permissions", tags=["Permission Endpoints"])


@router.post(
    "/",
    summary="Create a permission",
    description="Create a permission. only create by admin",
    response_model=PermissionRead,
    responses=ADMIN_WRITE,
)
async def create_permission(
    user: PermissionPolicy.Create,
    service: PermissionServiceDep,
    permission_in: PermissionCreate,
) -> Permission:
    return await service.create_permission(permission_in=permission_in)


@router.get(
    "/",
    summary="List permissions",
    description="List permissions. only access by admin",
    response_model=list[PermissionRead],
    responses=ADMIN_READ,
)
async def list_permissions(
    user: PermissionPolicy.List,
    service: PermissionServiceDep,
    limit: int = 20,
    offset: int = 0,
) -> Sequence[Permission]:
    return await service.list_permission(limit=limit, offset=offset)


@router.get(
    "/{permission_id}",
    summary="Get a permissions",
    description="Get a permissions. only access by admin",
    response_model=PermissionRead,
    responses=ADMIN_READ,
)
async def get_permission(
    user: PermissionPolicy.Read,
    service: PermissionServiceDep,
    permission_id: int,
) -> Permission:
    return await service.get_permission(permission_id=permission_id)


@router.patch(
    "/{permission_id}",
    summary="Update a permissions",
    description="Update a permissions. only access by admin",
    response_model=PermissionRead,
    responses=ADMIN_WRITE,
)
async def update_permission(
    user: PermissionPolicy.Update,
    service: PermissionServiceDep,
    permission_id: int,
    permission_in: PermissionUpdate,
) -> Permission:
    return await service.update_permission(
        permission_id=permission_id, permission_in=permission_in
    )


@router.delete(
    "/{permission_id}",
    summary="Delete a permissions",
    description="Delete a permissions. only access by admin",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=DELETE_RECORD,
)
async def delete_permission(
    user: PermissionPolicy.Delete,
    service: PermissionServiceDep,
    permission_id: int,
) -> None:
    return await service.delete_permission(permission_id=permission_id)
