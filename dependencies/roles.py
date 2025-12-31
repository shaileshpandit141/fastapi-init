from collections.abc import Callable
from typing import Annotated, Any, Iterable

from fastapi import Depends, HTTPException, status

from dependencies.user import ActiveUserDep
from models.user import User, UserRole


def require_roles(allowed_roles: Iterable[UserRole]) -> Callable[[ActiveUserDep], Any]:
    async def _checker(user: ActiveUserDep) -> User:
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return user

    return _checker


AdminUserDep = Annotated[User, Depends(require_roles([UserRole.ADMIN]))]
