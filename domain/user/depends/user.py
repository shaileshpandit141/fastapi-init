from typing import Annotated

from fastapi import Depends

from core.db.depends.async_session import AsyncSessionDep

from ..models.user import User
from ..services.user import UserService
from .authorization import authorize

# === User Service Dep ===


async def get_user_service(session: AsyncSessionDep) -> UserService:
    return UserService(session=session)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


# === Role-based deps ===


AdminUserDep = Annotated[User, Depends(authorize(roles=["admin"]))]
AuthenticatedUserDep = Annotated[User, Depends(authorize(roles=["user"]))]


# === Permission-based deps ===


UserCanCreateUserDep = Annotated[User, Depends(authorize(permissions=["user:create"]))]
UserCanReadUserDep = Annotated[User, Depends(authorize(permissions=["user:read"]))]
UserCanUpdateUserDep = Annotated[User, Depends(authorize(permissions=["user:update"]))]
UserCanDeleteUserDep = Annotated[User, Depends(authorize(permissions=["user:delete"]))]


# === Hybrid role + permission deps ===


AdminCanManageUsersDep = Annotated[
    User,
    Depends(
        authorize(
            roles=["admin"],
            permissions=[
                "user:read",
                "user:create",
                "user:update",
                "user:delete",
            ],
        )
    ),
]
