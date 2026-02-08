from typing import Annotated

from fastapi import Depends

from domain.authorization.depends import authorize
from domain.user.models import User

from .constants import NotificationPerm


class NotificationPolicy:
    """Authorization policies for Notification domain"""

    Create = Annotated[User, Depends(authorize(permissions=[NotificationPerm.CREATE]))]
    List = Annotated[User, Depends(authorize(permissions=[NotificationPerm.LIST]))]
    Read = Annotated[User, Depends(authorize(permissions=[NotificationPerm.READ]))]
    Update = Annotated[User, Depends(authorize(permissions=[NotificationPerm.UPDATE]))]
    Delete = Annotated[User, Depends(authorize(permissions=[NotificationPerm.DELETE]))]
