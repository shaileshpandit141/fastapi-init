from typing import Annotated

from fastapi import Depends

from core.db.depends.async_session import AsyncSessionDep
from domain.authorization.depends import authorize
from domain.user.models import User

from .services import UserRoleService, UserService

# === User Service Dep ===


async def get_user_service(session: AsyncSessionDep) -> UserService:
    return UserService(session=session)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


# === User Role Service Dep ===


async def get_user_role_service(session: AsyncSessionDep) -> UserRoleService:
    return UserRoleService(session=session)


UserRoleServiceDep = Annotated[UserRoleService, Depends(get_user_role_service)]

# === Role-based deps ===

CurrentUserDep = Annotated[User, Depends(authorize())]

UserDep = Annotated[User, Depends(authorize(roles=["user"]))]
AdminDep = Annotated[User, Depends(authorize(roles=["admin"]))]


# === Permission-based deps ===

CreateUserDep = Annotated[User, Depends(authorize(permissions=["user:create"]))]
ReadUserDep = Annotated[User, Depends(authorize(permissions=["user:read"]))]
UpdateUserDep = Annotated[User, Depends(authorize(permissions=["user:update"]))]
DeleteUserDep = Annotated[User, Depends(authorize(permissions=["user:delete"]))]


# === Hybrid role + permission deps ===

AdminManageUsersDep = Annotated[
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
