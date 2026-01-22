from typing import Sequence

from fastapi import APIRouter, status

from core.response.swagger import ADMIN_READ, ADMIN_WRITE, DELETE_RECORD
from domain.rbac.depends.require_access import AdminUserDep
from domain.rbac.depends.user_role import UserRoleServiceDep
from domain.rbac.models.user_role import UserRole
from domain.rbac.schemas.user_role import UserRoleCreate, UserRoleRead, UserRoleUpdate
from domain.user.depends.user import UserServiceDep
from domain.user.models.user import User
from domain.user.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["User Endpoints"])


# === User specific endpoints ===


@router.post(
    path="/",
    summary="Create a new user",
    description="Create a new user. Admin only.",
    response_model=UserRead,
    responses=ADMIN_WRITE,
)
async def create_user(
    user: AdminUserDep, user_service: UserServiceDep, user_in: UserCreate
) -> User:
    return await user_service.create_user(user_in=user_in)


@router.get(
    path="/",
    summary="Retrieve list of users",
    description="Retrieve list of users. Admin only.",
    response_model=list[UserRead],
    responses=ADMIN_READ,
)
async def list_user(
    user: AdminUserDep, user_service: UserServiceDep, limit: int = 20, offset: int = 0
) -> Sequence[User]:
    return await user_service.list_user(limit=limit, offset=offset)


@router.get(
    path="/{id}",
    summary="Retrieve a user",
    description="Retrieve a user by ID. Admin only.",
    response_model=UserRead,
    responses=ADMIN_READ,
)
async def read_user(user: AdminUserDep, user_service: UserServiceDep, id: int) -> User:
    return await user_service.get_user(id)


@router.patch(
    path="/{id}",
    summary="Update a user",
    description="Update user information. Admin only.",
    response_model=UserRead,
    responses=ADMIN_READ,
)
async def update_user(
    user: AdminUserDep, user_service: UserServiceDep, id: int, user_in: UserUpdate
) -> User:
    return await user_service.update_user(id, user_in)


@router.delete(
    path="/{id}",
    summary="Delete a user",
    description="Delete a user. Admin only.",
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
    summary="List user roles",
    description="List all roles assigned to a user. Admin only.",
    response_model=list[UserRoleRead],
    responses=ADMIN_READ,
)
async def list_user_roles(
    user: AdminUserDep, user_role_service: UserRoleServiceDep, id: int
) -> Sequence[UserRole]:
    return await user_role_service.list_user_roles(user_id=id)


@router.post(
    path="/{id}/roles/",
    summary="Create user role",
    description="Create user role. Admin only.",
    response_model=UserRoleRead,
    responses=ADMIN_READ,
)
async def create_user_role(
    user: AdminUserDep,
    user_role_service: UserRoleServiceDep,
    id: int,
    user_role_in: UserRoleCreate,
) -> UserRole:
    return await user_role_service.create_user_role(
        user_id=id, user_role_in=user_role_in
    )


@router.patch(
    path="/{id}/roles/",
    summary="Update user role",
    description="Update user role. Admin only.",
    response_model=UserRoleRead,
    responses=ADMIN_READ,
)
async def update_user_role(
    user: AdminUserDep,
    user_role_service: UserRoleServiceDep,
    id: int,
    user_role_in: UserRoleUpdate,
) -> UserRole:
    return await user_role_service.update_user_role(
        user_id=id, user_role_in=user_role_in
    )
