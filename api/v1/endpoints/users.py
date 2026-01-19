from typing import Sequence

from fastapi import APIRouter

from domain.rbac.depends.require_access import AdminUserDep
from domain.user.depends.user import UserServiceDep
from domain.user.models.user import User
from domain.user.schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["User Endpoints"])


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
