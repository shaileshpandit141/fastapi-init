from typing import Sequence

from fastapi import APIRouter, status

from core.swagger import Access, Action, openapi_docs
from domain.role.depends import RolePermissionServiceDep, RoleServiceDep
from domain.role.models import Role, RolePermission
from domain.role.policies import RolePermissionPolicy, RolePolicy
from domain.role.schemas import (
    RoleCreate,
    RolePermissionCreate,
    RolePermissionRead,
    RoleRead,
    RoleUpdate,
)

router = APIRouter(prefix="/roles", tags=["Role Endpoints"])


# === Roles specific endpoints ===


@router.post(
    path="/",
    response_model=RoleRead,
    **openapi_docs(
        action=Action.CREATE,
        resource="role",
        access=Access.AUTHENTICATED,
    ),
)
async def create_role(
    user: RolePolicy.Create, service: RoleServiceDep, role_in: RoleCreate
) -> Role:
    return await service.create_role(role_in=role_in)


@router.get(
    path="/",
    response_model=list[RoleRead],
    **openapi_docs(
        action=Action.LIST,
        resource="roles",
        access=Access.AUTHENTICATED,
    ),
)
async def list_roles(
    user: RolePolicy.List,
    service: RoleServiceDep,
    limit: int = 20,
    offset: int = 0,
) -> Sequence[Role]:
    return await service.list_roles(limit=limit, offset=offset)


@router.get(
    path="/{role_id}",
    response_model=RoleRead,
    **openapi_docs(
        action=Action.RETRIEVE,
        resource="role",
        access=Access.AUTHENTICATED,
    ),
)
async def read_role(
    user: RolePolicy.Read,
    service: RoleServiceDep,
    role_id: int,
) -> Role:
    return await service.get_role(role_id=role_id)


@router.patch(
    path="/{role_id}",
    response_model=RoleRead,
    **openapi_docs(
        action=Action.UPDATE,
        resource="role",
        access=Access.AUTHENTICATED,
    ),
)
async def update_role(
    user: RolePolicy.Update,
    service: RoleServiceDep,
    role_id: int,
    role_in: RoleUpdate,
) -> Role:
    return await service.update_role(role_id=role_id, role_in=role_in)


@router.patch(
    path="/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    **openapi_docs(
        action=Action.DELETE,
        resource="role",
        access=Access.AUTHENTICATED,
    ),
)
async def delete_role(
    user: RolePolicy.Update,
    service: RoleServiceDep,
    role_id: int,
) -> None:
    await service.delete_role(role_id=role_id)


# === Permission Assignment endpoints ===


@router.post(
    path="/{role_id}/permissions/",
    response_model=RolePermissionRead,
    **openapi_docs(
        action=Action.CREATE,
        resource="role-permission",
        access=Access.AUTHENTICATED,
    ),
)
async def assign_role_permission(
    user: RolePermissionPolicy.Assign,
    service: RolePermissionServiceDep,
    role_id: int,
    role_permission_in: RolePermissionCreate,
) -> RolePermission:
    return await service.create_role_permission(
        role_id=role_id,
        role_permission_in=role_permission_in,
    )


@router.get(
    path="/{role_id}/permissions/",
    response_model=list[RolePermissionRead],
    **openapi_docs(
        action=Action.LIST,
        resource="role-permissions",
        access=Access.AUTHENTICATED,
    ),
)
async def list_role_permissions(
    user: RolePermissionPolicy.List,
    service: RolePermissionServiceDep,
    role_id: int,
    limit: int = 20,
    offset: int = 0,
) -> Sequence[RolePermission]:
    return await service.list_role_permission(
        role_id=role_id, limit=limit, offset=offset
    )


@router.delete(
    path="/{role_id}/permissions/{permission_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    **openapi_docs(
        action=Action.DELETE,
        resource="role-permission",
        access=Access.AUTHENTICATED,
    ),
)
async def revoke_role_permission(
    user: RolePermissionPolicy.Revoke,
    service: RolePermissionServiceDep,
    role_id: int,
    permission_id: int,
) -> None:
    await service.delete_role_permission(
        role_id=role_id,
        permission_id=permission_id,
    )
