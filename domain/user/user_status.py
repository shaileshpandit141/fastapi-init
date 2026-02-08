from abc import ABC, abstractmethod

from core.exceptions.http_exception import AccessDeniedError

from .constants import UserStatus
from .models import User


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


USER_STATE_MAP: dict[UserStatus, UserState] = {
    UserStatus.ACTIVE: ActiveState(),
    UserStatus.PENDING: PendingState(),
    UserStatus.INACTIVE: InactiveState(),
    UserStatus.SUSPENDED: SuspendedState(),
    UserStatus.BANNED: BannedState(),
}
