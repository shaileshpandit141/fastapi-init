from typing import Iterable

from core.exceptions import AccessDeniedException
from domain.authentication.services import CurrentUserService
from domain.user.models import User


def permission_matches(granted: str, required: str) -> bool:
    if granted == required:
        return True

    if granted.endswith(":*"):
        prefix = granted[:-2]
        return required.startswith(prefix + ":")

    return False


class AuthorizationService:
    def __init__(self, current_user: CurrentUserService) -> None:
        self._current_user = current_user

    async def authorize(
        self,
        *,
        roles: Iterable[str] | None = None,
        permissions: Iterable[str] | None = None,
    ) -> User:
        user = await self._current_user.get_active_user()

        roles = set(roles or [])
        permissions = set(permissions or [])

        # ---- Role check ----
        if roles:
            user_roles = {ur.role.name for ur in user.roles}
            if not user_roles.intersection(roles):
                raise AccessDeniedException(detail="Access denied")

        # ---- Permission check (with wildcard support) ----
        if permissions:
            user_permissions = {
                rp.permission.code for ur in user.roles for rp in ur.role.permissions
            }

            for required in permissions:
                if not any(
                    permission_matches(granted, required)
                    for granted in user_permissions
                ):
                    raise AccessDeniedException(detail="Access denied")

        return user
