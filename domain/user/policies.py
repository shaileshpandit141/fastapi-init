from typing import Annotated

from fastapi import Depends

from domain.authorization.depends import authorize
from domain.permission.constants import UserPerm, UserRolePerm
from domain.user.models import User


class UserPolicy:
    """Authorization policies for User domain"""

    Create = Annotated[User, Depends(authorize(permissions=[UserPerm.CREATE]))]
    List = Annotated[User, Depends(authorize(permissions=[UserPerm.LIST]))]
    Read = Annotated[User, Depends(authorize(permissions=[UserPerm.READ]))]
    Update = Annotated[User, Depends(authorize(permissions=[UserPerm.UPDATE]))]
    Delete = Annotated[User, Depends(authorize(permissions=[UserPerm.DELETE]))]


class UserRolePolicy:
    """Authorization policies for User-Role assignments"""

    Assign = Annotated[User, Depends(authorize(permissions=[UserRolePerm.ASSIGN]))]
    List = Annotated[User, Depends(authorize(permissions=[UserRolePerm.LIST]))]
    Revoke = Annotated[User, Depends(authorize(permissions=[UserRolePerm.REVOKE]))]
