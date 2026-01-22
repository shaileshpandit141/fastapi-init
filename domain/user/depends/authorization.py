from typing import Annotated, Awaitable, Callable, Iterable

from fastapi import Depends

from ..models.user import User
from ..services.authorization import AuthorizationService
from .current_user import CurrentUserServiceDep

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
