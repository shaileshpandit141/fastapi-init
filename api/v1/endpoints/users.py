from typing import Sequence

from fastapi import APIRouter, status

from core.response.schemas import DetailResponse
from core.response.swagger import (
    ADMIN_READ,
    ADMIN_WRITE,
    DELETE_RECORD,
    OpenAPIResponses,
)
from domain.rbac.depends.require_access import AdminUserDep
from domain.rbac.depends.user_role import UserRoleServiceDep
from domain.rbac.models.user_role import UserRole
from domain.rbac.schemas.user_role import UserRoleRead
from domain.user.depends.user import UserServiceDep
from domain.user.models.user import User
from domain.user.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["User Endpoints"])


# === User specific endpoints ===


@router.post(
    path="/",
    summary="Create a new user",
    description="Create a new user. Only created by admin.",
    response_model=UserRead,
    responses=ADMIN_WRITE,
)
async def create_user(
    user: AdminUserDep, user_service: UserServiceDep, user_in: UserCreate
) -> User:
    return await user_service.create_user(user_in=user_in)


@router.get(
    path="/",
    summary="Retrive list of users",
    description="Retrive list of users. Only access by admin.",
    response_model=list[UserRead],
    responses=ADMIN_READ,
)
async def list_user(
    user: AdminUserDep, user_service: UserServiceDep, limit: int = 20, offset: int = 0
) -> Sequence[User]:
    return await user_service.list_user(limit=limit, offset=offset)


@router.get(
    path="/{id}",
    summary="Retrive a user",
    description="Retrive a user. Only retrive by admin.",
    response_model=UserRead,
    responses=ADMIN_READ,
)
async def read_user(user: AdminUserDep, user_service: UserServiceDep, id: int) -> User:
    return await user_service.get_user(id)


@router.patch(
    path="/{id}",
    summary="Update a user info",
    description="Update a user info. Only admin can update.",
    response_model=UserRead,
    responses=ADMIN_READ,
)
async def update_user(
    user: AdminUserDep, user_service: UserServiceDep, id: int, user_in: UserUpdate
) -> User:
    return await user_service.update_user(id, user_in)


DELETE_RESPONSES: OpenAPIResponses = {
    204: {"description": "No Content"},
    404: {"model": DetailResponse, "description": "User does not exist."},
}


@router.delete(
    path="/{id}",
    summary="Delete a user",
    description="Delete a user. Only admin can delete.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=DELETE_RECORD,
)
async def delete_user(
    user: AdminUserDep, user_service: UserServiceDep, id: int
) -> None:
    return await user_service.delete_user(id)


# === RBAC specific endpoints ===


@router.get(
    path="/{id}/roles/",
    summary="List all user roles",
    description="List all user roles. Only access by admin.",
    response_model=list[UserRoleRead],
    responses=ADMIN_READ,
)
async def list_user_roles(
    user: AdminUserDep, user_role_service: UserRoleServiceDep, id: int
) -> Sequence[UserRole]:
    return await user_role_service.list_user_roles(user_id=id)
