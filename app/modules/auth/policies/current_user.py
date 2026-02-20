from abc import ABC, abstractmethod

from app.adapters.db.models.user import User
from app.core.exceptions import AccessDeniedError
from app.shared.enums.user import UserStatus


class UserState(ABC):
    @abstractmethod
    def ensure_access(self, user: User) -> None:
        pass


class ActiveState(UserState):
    def ensure_access(self, user: "User") -> None:
        if not user.is_email_verified:
            raise AccessDeniedError("Please verify your email.")


class PendingState(UserState):
    def ensure_access(self, user: "User") -> None:
        raise AccessDeniedError("Account not activated yet.")


class InactiveState(UserState):
    def ensure_access(self, user: "User") -> None:
        raise AccessDeniedError("Account is inactive.")


class SuspendedState(UserState):
    def ensure_access(self, user: "User") -> None:
        raise AccessDeniedError("Account is suspended.")


class BannedState(UserState):
    def ensure_access(self, user: "User") -> None:
        raise AccessDeniedError("Account has been banned.")


CURRENT_USER_POLICY_MAP: dict[UserStatus, UserState] = {
    UserStatus.ACTIVE: ActiveState(),
    UserStatus.PENDING: PendingState(),
    UserStatus.INACTIVE: InactiveState(),
    UserStatus.SUSPENDED: SuspendedState(),
    UserStatus.BANNED: BannedState(),
}
