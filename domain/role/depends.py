from typing import Annotated

from fastapi import Depends

from core.db.depends.async_session import AsyncSessionDep
from domain.authorization.depends import authorize
from domain.user.models import User

from .services import RolePermissionService, RoleService

# === Service dependencies ===


async def get_role_service(session: AsyncSessionDep) -> RoleService:
    return RoleService(session=session)


async def get_role_permission_service(
    session: AsyncSessionDep,
) -> RolePermissionService:
    return RolePermissionService(session=session)


class RoleServices:
    """
    Access to role-related domain services
    """

    Role = Annotated[RoleService, Depends(get_role_service)]
    RolePermission = Annotated[
        RolePermissionService, Depends(get_role_permission_service)
    ]


# === Permission-based access (Permission model) ===


class RolePermissions:
    """
    Fine-grained permissions for Role CRUD
    """

    Create = Annotated[User, Depends(authorize(permissions=["role:create"]))]
    Read = Annotated[User, Depends(authorize(permissions=["role:read"]))]
    Update = Annotated[User, Depends(authorize(permissions=["role:update"]))]
    Delete = Annotated[User, Depends(authorize(permissions=["role:delete"]))]


class RolePermissionAssignments:
    """
    Permissions for assigning and revoking permissions from roles
    """

    Assign = Annotated[User, Depends(authorize(permissions=["role:permission:assign"]))]
    Revoke = Annotated[User, Depends(authorize(permissions=["role:permission:revoke"]))]
    List = Annotated[User, Depends(authorize(permissions=["role:permission:list"]))]


# === Hybrid (role + permission) access ===


class RoleAccess:
    """
    Full access to Role domain
    """

    Admin = Annotated[User, Depends(authorize(roles=["admin"], permissions=["role:*"]))]


class RolePermissionAssignmentAccess:
    """
    Full access to User ↔ Role assignments
    """

    Admin = Annotated[
        User, Depends(authorize(roles=["admin"], permissions=["role:permission:*"]))
    ]
