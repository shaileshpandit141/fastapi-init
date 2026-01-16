from typing import Annotated, Awaitable, Callable, Iterable

from fastapi import Depends

from domain.user.deps import CurrentUserServiceDep
from domain.user.models import User

from ..services.require_access import RequireAccessService

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


# === Role-based deps ===


AdminUserDep = Annotated[User, Depends(require_access(roles=["admin"]))]


# === Permission-based deps ===


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


# === Combined permissions deps ===


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


# === Hybrid role + permission deps ===


AdminCanManageUsersDep = Annotated[
    User, Depends(require_access(roles=["admin"], permissions=["user:delete"]))
]
