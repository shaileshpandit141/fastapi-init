from typing import Awaitable, Callable, Iterable

from fastapi import Depends

from domain.authentication.depends import CurrentUserServiceDep
from domain.user.models import User

from .services import AuthorizationService

# === Authorization Service Dep ===


async def get_authorization_service(
    current_user_service: CurrentUserServiceDep,
) -> AuthorizationService:
    return AuthorizationService(current_user_service)


# === authorize service Dep ===


def authorize(
    *, roles: Iterable[str] | None = None, permissions: Iterable[str] | None = None
) -> Callable[..., Awaitable[User]]:

    async def _checker(
        authorization_service: AuthorizationService = Depends(
            get_authorization_service
        ),
    ) -> User:
        return await authorization_service.authorize(
            roles=roles, permissions=permissions
        )

    return _checker
