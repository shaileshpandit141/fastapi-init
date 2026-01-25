from typing import Annotated

from fastapi import Depends

from domain.authorization.depends import authorize
from domain.permission.constants import RolePerm, RolePermissionPerm
from domain.user.models import User


class RolePolicy:
    """Authorization policies for Role domain"""

    Create = Annotated[User, Depends(authorize(permissions=[RolePerm.CREATE]))]
    List = Annotated[User, Depends(authorize(permissions=[RolePerm.LIST]))]
    Read = Annotated[User, Depends(authorize(permissions=[RolePerm.READ]))]
    Update = Annotated[User, Depends(authorize(permissions=[RolePerm.UPDATE]))]
    Delete = Annotated[User, Depends(authorize(permissions=[RolePerm.DELETE]))]


class RolePermissionPolicy:
    """Authorization policies for Role-Permission assignments"""

    Assign = Annotated[
        User,
        Depends(authorize(permissions=[RolePermissionPerm.ASSIGN])),
    ]
    Revoke = Annotated[
        User,
        Depends(authorize(permissions=[RolePermissionPerm.REVOKE])),
    ]
    List = Annotated[
        User,
        Depends(authorize(permissions=[RolePermissionPerm.LIST])),
    ]
