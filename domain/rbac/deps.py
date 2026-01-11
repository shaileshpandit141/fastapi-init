from collections.abc import Callable, Iterable
from typing import Annotated, Awaitable

from fastapi import Depends, HTTPException, status

from domain.user.deps import ActiveUserDep
from domain.user.models import User


def require_roles(
    allowed_roles: Iterable[str],
) -> Callable[[ActiveUserDep], Awaitable[User]]:
    allowed_roles_set = set(allowed_roles)

    async def _checker(user: ActiveUserDep) -> User:
        user_role_names: set[str] = {link.role.name for link in user.roles}

        if not user_role_names.intersection(allowed_roles_set):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return user

    return _checker


def require_permissions(
    required: Iterable[str],
) -> Callable[[ActiveUserDep], Awaitable[User]]:
    required_set = set(required)

    async def _checker(user: ActiveUserDep) -> User:
        user_permissions: set[str] = {
            perm.permission.code
            for role_link in user.roles
            for perm in role_link.role.permissions
        }

        if required_set - user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return user

    return _checker


UserDep = Annotated[User, Depends(require_roles(["user"]))]
AdminUserDep = Annotated[User, Depends(require_roles(["admin"]))]


CanCreateUsersDep = Annotated[User, Depends(require_permissions(["users.create"]))]
CanReadUsersDep = Annotated[User, Depends(require_permissions(["users.read"]))]
CanUpdateUsersDep = Annotated[User, Depends(require_permissions(["users.update"]))]
CanDeleteUsersDep = Annotated[User, Depends(require_permissions(["users.delete"]))]
