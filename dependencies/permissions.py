from collections.abc import Callable, Iterable
from typing import Annotated, Awaitable

from fastapi import Depends, HTTPException, status

from dependencies.user import ActiveUserDep
from models.user import User


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


CanCreateUsersDep = Annotated[User, Depends(require_permissions(["users.create"]))]
CanReadUsersDep = Annotated[User, Depends(require_permissions(["users.read"]))]
CanUpdateUsersDep = Annotated[User, Depends(require_permissions(["users.update"]))]
CanDeleteUsersDep = Annotated[User, Depends(require_permissions(["users.delete"]))]
