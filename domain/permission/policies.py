from typing import Annotated

from fastapi import Depends

from domain.authorization.depends import authorize
from domain.permission.constants import PermissionPerm
from domain.role.constants import RoleType
from domain.user.models import User


class PermissionPolicy:
    """Authorization policies for Permission domain"""

    Create = Annotated[User, Depends(authorize(permissions=[PermissionPerm.CREATE]))]
    Read = Annotated[User, Depends(authorize(permissions=[PermissionPerm.READ]))]
    Update = Annotated[User, Depends(authorize(permissions=[PermissionPerm.UPDATE]))]
    Delete = Annotated[User, Depends(authorize(permissions=[PermissionPerm.DELETE]))]

    Admin = Annotated[
        User,
        Depends(
            authorize(
                roles=[RoleType.ADMIN],
                permissions=[PermissionPerm.FULL],
            )
        ),
    ]
