from app.adapters.db.models.user import User
from app.core.exceptions.http import PermissionDeniedError
from app.shared.enums.permission import PermissionEnum


class UserPolicy:
    """Enforces business rules related to User."""

    @staticmethod
    def enforce_permission(user: User, permission: PermissionEnum) -> None:
        if not user.has_permission(permission):
            raise PermissionDeniedError("Insufficient permissions")

    @staticmethod
    def enforce_can_modify_user(actor: User, target: User) -> None:
        if actor.is_superadmin():
            return

        if actor.id == target.id:
            return  # allow self-modification

        raise PermissionDeniedError("Not allowed to modify this user")

    @staticmethod
    def enforce_can_delete_user(actor: User, target: User) -> None:
        if actor.is_superadmin():
            return

        raise PermissionDeniedError("Only superadmin can delete users")
