from typing import Sequence

from fastapi import APIRouter

from domain.rbac.depends.require_access import AdminUserDep
from domain.user.depends.user import UserServiceDep
from domain.user.models.user import User
from domain.user.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["User Endpoints"])


@router.post(
    path="/",
    summary="Create a new user",
    description="Create a new user. Only created by admin.",
    response_model=UserRead,
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
)
async def read_user(user: AdminUserDep, user_service: UserServiceDep, id: int) -> User:
    return await user_service.get_user(id)
