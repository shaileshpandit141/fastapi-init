from typing import Annotated, Awaitable, Callable, Iterable

from fastapi import Depends

from core.db.deps import AsyncSessionDep
from domain.user.deps import CurrentUserServiceDep
from domain.user.models import User

from .models import Permission, Role, RolePermission, UserRole
from .repository import (
    PermissionRepository,
    RolePermissionRepository,
    RoleRepository,
    UserRoleRepository,
)
from .service import (
    PermissionService,
    RequireAccessService,
    RolePermissionService,
    RoleService,
    UserRoleService,
)

# === Role Service Dep ===


async def get_role_service(session: AsyncSessionDep) -> RoleService:
    return RoleService(RoleRepository(model=Role, session=session))


RoleServiceDep = Annotated[RoleService, Depends(get_role_service)]


# === Permission Service Dep ===


async def get_permission_service(session: AsyncSessionDep) -> PermissionService:
    return PermissionService(PermissionRepository(model=Permission, session=session))


PermissionServiceDep = Annotated[PermissionService, Depends(get_permission_service)]


# === Role Permission Service Dep ===


async def get_role_permission_service(
    session: AsyncSessionDep,
) -> RolePermissionService:
    return RolePermissionService(
        RolePermissionRepository(model=RolePermission, session=session)
    )


RolePermissionServiceDep = Annotated[
    RolePermissionService, Depends(get_role_permission_service)
]


# === User Role Service Dep ===


async def get_user_role_service(session: AsyncSessionDep) -> UserRoleService:
    return UserRoleService(UserRoleRepository(model=UserRole, session=session))


UserRoleServiceDep = Annotated[UserRoleService, Depends(get_user_role_service)]


# === Require Access Service Dep ===


async def get_require_access_service(
    current_user_service: CurrentUserServiceDep,
) -> RequireAccessService:
    return RequireAccessService(current_user_service)


RequireAccessServiceDep = Annotated[
    RequireAccessService, Depends(get_require_access_service)
]


# === Require Access Dep ===


def require_access(
    *, roles: Iterable[str] | None = None, permissions: Iterable[str] | None = None
) -> Callable[..., Awaitable[User]]:

    async def _checker(
        require_access_service: RequireAccessServiceDep,
    ) -> User:
        return await require_access_service.require_access(
            roles=roles,
            permissions=permissions,
        )

    return _checker


# --- Role-based deps ---


AdminUserDep = Annotated[User, Depends(require_access(roles=["admin"]))]


# --- Permission-based deps ---


UserCanCreateUserDep = Annotated[
    User, Depends(require_access(permissions=["user:create"]))
]
UserCanReadUserDep = Annotated[User, Depends(require_access(permissions=["user:read"]))]
UserCanUpdateUserDep = Annotated[
    User, Depends(require_access(permissions=["user:update"]))
]
UserCanDeleteUserDep = Annotated[
    User, Depends(require_access(permissions=["user:delete"]))
]


# --- Combined permissions deps ---


UserCanManageUsersDep = Annotated[
    User,
    Depends(
        require_access(
            permissions=[
                "user:read",
                "user:create",
                "user:update",
                "user:delete",
            ],
        )
    ),
]


# --- Hybrid role + permission deps ---


AdminCanManageUsersDep = Annotated[
    User, Depends(require_access(roles=["admin"], permissions=["user:delete"]))
]
