from typing import Sequence

from fastapi import APIRouter, status

from core.swagger import Access, Action, openapi_docs
from domain.permission.depends import PermissionServiceDep
from domain.permission.models import Permission
from domain.permission.policies import PermissionPolicy
from domain.permission.schemas import PermissionCreate, PermissionRead, PermissionUpdate

router = APIRouter(prefix="/permissions", tags=["Permission Endpoints"])


@router.post(
    path="/",
    response_model=PermissionRead,
    **openapi_docs(
        action=Action.CREATE,
        resource="permission",
        access=Access.AUTHENTICATED,
    ),
)
async def create_permission(
    user: PermissionPolicy.Create,
    service: PermissionServiceDep,
    permission_in: PermissionCreate,
) -> Permission:
    return await service.create_permission(permission_in=permission_in)


@router.get(
    path="/",
    response_model=list[PermissionRead],
    **openapi_docs(
        action=Action.LIST,
        resource="permissions",
        access=Access.AUTHENTICATED,
    ),
)
async def list_permissions(
    user: PermissionPolicy.List,
    service: PermissionServiceDep,
    limit: int = 20,
    offset: int = 0,
) -> Sequence[Permission]:
    return await service.list_permission(limit=limit, offset=offset)


@router.get(
    path="/{permission_id}",
    response_model=PermissionRead,
    **openapi_docs(
        action=Action.RETRIEVE,
        resource="permission",
        access=Access.AUTHENTICATED,
    ),
)
async def read_permission(
    user: PermissionPolicy.Read,
    service: PermissionServiceDep,
    permission_id: int,
) -> Permission:
    return await service.get_permission(permission_id=permission_id)


@router.patch(
    path="/{permission_id}",
    response_model=PermissionRead,
    **openapi_docs(
        action=Action.UPDATE,
        resource="permission",
        access=Access.AUTHENTICATED,
    ),
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
    path="/{permission_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    **openapi_docs(
        action=Action.DELETE,
        resource="permission",
        access=Access.AUTHENTICATED,
    ),
)
async def delete_permission(
    user: PermissionPolicy.Delete,
    service: PermissionServiceDep,
    permission_id: int,
) -> None:
    return await service.delete_permission(permission_id=permission_id)
