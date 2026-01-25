from typing import Annotated

from fastapi import Depends

from domain.authorization.depends import authorize
from domain.permission.constants import UserPerm, UserRolePerm
from domain.role.constants import RoleType
from domain.user.models import User


class UserPolicy:
    """Authorization policies for User domain"""

    Create = Annotated[User, Depends(authorize(permissions=[UserPerm.CREATE]))]
    Read = Annotated[User, Depends(authorize(permissions=[UserPerm.READ]))]
    Update = Annotated[User, Depends(authorize(permissions=[UserPerm.UPDATE]))]
    Delete = Annotated[User, Depends(authorize(permissions=[UserPerm.DELETE]))]

    Admin = Annotated[
        User,
        Depends(
            authorize(
                roles=[RoleType.ADMIN],
                permissions=[UserPerm.FULL],
            )
        ),
    ]


class UserRolePolicy:
    """Authorization policies for User-Role assignments"""

    Assign = Annotated[User, Depends(authorize(permissions=[UserRolePerm.ASSIGN]))]
    Revoke = Annotated[User, Depends(authorize(permissions=[UserRolePerm.REVOKE]))]
    List = Annotated[User, Depends(authorize(permissions=[UserRolePerm.LIST]))]

    Admin = Annotated[
        User,
        Depends(
            authorize(
                roles=[RoleType.ADMIN],
                permissions=[UserRolePerm.FULL],
            )
        ),
    ]
