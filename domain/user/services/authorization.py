from typing import Iterable

from core.exceptions import AccessDeniedException

from ..models.user import User
from .current_user import CurrentUserService

# === User Authorization Service ===


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

        if roles:
            user_roles = {ur.role.name for ur in user.roles}
            if not user_roles.intersection(roles):
                raise AccessDeniedException(detail="Access denied")

        if permissions:
            user_permissions = {
                rp.permission.code for ur in user.roles for rp in ur.role.permissions
            }
            if not permissions.issubset(user_permissions):
                raise AccessDeniedException(detail="Access denied")

        return user
