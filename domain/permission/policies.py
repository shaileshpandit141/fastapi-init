from typing import Annotated

from fastapi import Depends

from domain.authorization.depends import authorize
from domain.permission.constants import PermissionPerm
from domain.user.models import User


class PermissionPolicy:
    """Authorization policies for Permission domain"""

    Create = Annotated[User, Depends(authorize(permissions=[PermissionPerm.CREATE]))]
    List = Annotated[User, Depends(authorize(permissions=[PermissionPerm.LIST]))]
    Read = Annotated[User, Depends(authorize(permissions=[PermissionPerm.READ]))]
    Update = Annotated[User, Depends(authorize(permissions=[PermissionPerm.UPDATE]))]
    Delete = Annotated[User, Depends(authorize(permissions=[PermissionPerm.DELETE]))]
