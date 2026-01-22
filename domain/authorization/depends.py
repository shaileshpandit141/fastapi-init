from typing import Annotated, Awaitable, Callable, Iterable

from fastapi import Depends

from domain.user.depends import CurrentUserServiceDep
from domain.user.models import User

from .services import AuthorizationService

# === Require Access Service Dep ===


async def get_authorization_service(
    current_user_service: CurrentUserServiceDep,
) -> AuthorizationService:
    return AuthorizationService(current_user_service)


AuthorizationServiceDep = Annotated[
    AuthorizationService, Depends(get_authorization_service)
]

# === Require Access Dep ===


def authorize(
    *, roles: Iterable[str] | None = None, permissions: Iterable[str] | None = None
) -> Callable[..., Awaitable[User]]:

    async def _checker(
        authorization_service: AuthorizationServiceDep,
    ) -> User:
        return await authorization_service.authorize(
            roles=roles, permissions=permissions
        )

    return _checker


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
