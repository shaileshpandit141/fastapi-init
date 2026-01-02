from collections.abc import Callable, Iterable
from typing import Annotated, Awaitable

from fastapi import Depends, HTTPException, status

from dependencies.user import ActiveUserDep
from models.user import User


def require_roles(
    allowed_roles: Iterable[str],
) -> Callable[[ActiveUserDep], Awaitable[User]]:
    allowed_roles_set = set(allowed_roles)

    async def _checker(user: ActiveUserDep) -> User:
        user_role_names = {link.role.name for link in user.roles}

        if not user_role_names.intersection(allowed_roles_set):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return user

    return _checker


AdminUserDep = Annotated[User, Depends(require_roles(["admins"]))]
