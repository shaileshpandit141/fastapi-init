from typing import Annotated

from fastapi import Depends

from domain.authorization.depends import authorize
from domain.permission.constants import Perm
from domain.role.constants import Role
from domain.user.models import User


class UserAccessPolicy:
    """Authorization policies for User domain"""

    Create = Annotated[User, Depends(authorize(permissions=[Perm.User.CREATE]))]
    Read = Annotated[User, Depends(authorize(permissions=[Perm.User.READ]))]
    Update = Annotated[User, Depends(authorize(permissions=[Perm.User.UPDATE]))]
    Delete = Annotated[User, Depends(authorize(permissions=[Perm.User.DELETE]))]

    Admin = Annotated[
        User,
        Depends(
            authorize(
                roles=[Role.ADMIN],
                permissions=[Perm.User.FULL],
            )
        ),
    ]


class UserRoleAccessPolicy:
    """Authorization policies for User-Role assignments"""

    Assign = Annotated[User, Depends(authorize(permissions=[Perm.UserRole.ASSIGN]))]
    Revoke = Annotated[User, Depends(authorize(permissions=[Perm.UserRole.REVOKE]))]
    List = Annotated[User, Depends(authorize(permissions=[Perm.UserRole.LIST]))]

    Admin = Annotated[
        User,
        Depends(
            authorize(
                roles=[Role.ADMIN],
                permissions=[Perm.UserRole.FULL],
            )
        ),
    ]
