from app.adapters.db.models.user import User
from app.core.exceptions.http import PermissionDeniedError
from app.shared.enums.user import UserStatusEnum


class LoginPolicy:
    """Enforces business rules related to User."""

    @staticmethod
    def enforce_can_login(user: User) -> None:
        if user.is_superadmin():
            return

        if user.status is not UserStatusEnum.ACTIVE:
            raise PermissionDeniedError("User is not active")

        if not user.is_email_verified:
            raise PermissionDeniedError("Email is not verified")
