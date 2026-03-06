from app.adapters.db.models.user import User
from app.core.exceptions.http import PermissionDeniedError
from app.shared.enums.permission import PermissionEnum

from ..queries.list import ListUserQuery


class ListUserPolicy:
    async def __call__(self, actor: User, query: ListUserQuery) -> None:
        if not actor.has_permission(PermissionEnum.USER_LIST):
            raise PermissionDeniedError("Permission denied.")
