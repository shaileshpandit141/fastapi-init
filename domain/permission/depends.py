from typing import Annotated

from fastapi import Depends

from core.db.depends import AsyncSessionDep
from domain.authorization.depends import authorize
from domain.user.models import User

from .services import PermissionService

# === Service dependencies ===


async def get_permission_service(session: AsyncSessionDep) -> PermissionService:
    return PermissionService(session=session)


class PermissionServices:
    """
    Access to permission-related domain services
    """

    Permission = Annotated[PermissionService, Depends(get_permission_service)]


# === Permission-based access (Permission model) ===


class PermPermissions:
    """
    Fine-grained permissions for Permission CRUD
    """

    Create = Annotated[User, Depends(authorize(permissions=["permission:create"]))]
    Read = Annotated[User, Depends(authorize(permissions=["permission:read"]))]
    Update = Annotated[User, Depends(authorize(permissions=["permission:update"]))]
    Delete = Annotated[User, Depends(authorize(permissions=["permission:delete"]))]


# === Hybrid (role + permission) access ===


class PermissionAccess:
    """
    Full access to Permission domain
    """

    Admin = Annotated[
        User, Depends(authorize(roles=["admin"], permissions=["permission:*"]))
    ]
