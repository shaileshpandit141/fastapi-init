from typing import Annotated

from fastapi import Depends

from core.db.depends.async_session import AsyncSessionDep
from domain.authorization.depends import authorize
from domain.user.models import User

from .services import UserRoleService, UserService

# === Service dependencies ===


async def get_user_service(session: AsyncSessionDep) -> UserService:
    return UserService(session=session)


async def get_user_role_service(session: AsyncSessionDep) -> UserRoleService:
    return UserRoleService(session=session)


class UserServices:
    """
    Access to user-related domain services
    """

    User = Annotated[UserService, Depends(get_user_service)]
    Roles = Annotated[UserRoleService, Depends(get_user_role_service)]


# === Current user ===


class CurrentUser:
    """
    Currently authenticated user
    """

    Authenticated = Annotated[User, Depends(authorize())]


# === Role-based access ===


class UserRoleAccess:
    """
    Role-based access control
    """

    User = Annotated[User, Depends(authorize(roles=["user"]))]
    Admin = Annotated[User, Depends(authorize(roles=["admin"]))]


# === Permission-based access (User model) ===


class UserPermissions:
    """
    Fine-grained permissions for User CRUD
    """

    Create = Annotated[User, Depends(authorize(permissions=["user:create"]))]
    Read = Annotated[User, Depends(authorize(permissions=["user:read"]))]
    Update = Annotated[User, Depends(authorize(permissions=["user:update"]))]
    Delete = Annotated[User, Depends(authorize(permissions=["user:delete"]))]


# === User ↔ Role relationship permissions ===


class UserRoleAssignments:
    """
    Permissions for assigning and revoking roles from users
    """

    Assign = Annotated[User, Depends(authorize(permissions=["user:role:assign"]))]
    Revoke = Annotated[User, Depends(authorize(permissions=["user:role:revoke"]))]
    List = Annotated[User, Depends(authorize(permissions=["user:role:list"]))]


# === Hybrid (role + permission) access ===


class UserAccess:
    """
    Full access to User domain
    """

    Admin = Annotated[User, Depends(authorize(roles=["admin"], permissions=["user:*"]))]


class UserRoleAssignmentAccess:
    """
    Full access to User ↔ Role assignments
    """

    Admin = Annotated[
        User, Depends(authorize(roles=["admin"], permissions=["user:role:*"]))
    ]
