from typing import Iterable

from fastapi import HTTPException, status

from domain.user.models import User
from domain.user.services.current_user import CurrentUserService

# === Require Access Service ===


class RequireAccessService:
    def __init__(self, current_user_service: CurrentUserService) -> None:
        self.current_user_service = current_user_service

    async def require_access(
        self,
        *,
        roles: Iterable[str] | None = None,
        permissions: Iterable[str] | None = None,
    ) -> User:
        return await self._require_user_access(
            roles=roles,
            permissions=permissions,
        )

    async def _require_user_access(
        self,
        *,
        roles: Iterable[str] | None = None,
        permissions: Iterable[str] | None = None,
    ) -> User:
        user = await self.current_user_service.get_active_user()

        # --- Role check ---
        if roles:
            user_roles = {ur.role.name for ur in user.roles}

            if not user_roles.intersection(roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions",
                )

        # --- Permission check ---
        if permissions:
            user_permissions = {
                rp.permission.code for ur in user.roles for rp in ur.role.permissions
            }

            if not set(permissions).issubset(user_permissions):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions",
                )

        return user
