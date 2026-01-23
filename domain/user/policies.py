from core.exceptions import AccessDeniedException
from domain.user.models import User


class UserPolicy:
    @staticmethod
    def _is_admin(*, user: User) -> bool:
        return any(ur.role.name == "admin" for ur in user.roles)

    @classmethod
    def can_read(cls, *, actor: User, target: User) -> None:
        if cls._is_admin(user=actor):
            return

        if actor.id != target.id:
            raise AccessDeniedException(detail="You are not allowed to read this user")

    @classmethod
    def can_update(cls, *, actor: User, target: User) -> None:
        if cls._is_admin(user=actor):
            return

        if actor.id != target.id:
            raise AccessDeniedException(
                detail="You are not allowed to update this user"
            )

    @classmethod
    def can_delete(cls, *, actor: User, target: User) -> None:
        if cls._is_admin(user=actor):
            return

        if actor.id != target.id:
            raise AccessDeniedException(
                detail="You are not allowed to delete this user"
            )
