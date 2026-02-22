from abc import ABC, abstractmethod

from app.adapters.db.models.user import User
from app.shared.enums.user import UserStatusEnum

from ..exceptions import AccessDeniedError


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


class SuspendedState(UserState):
    def ensure_access(self, user: "User") -> None:
        raise AccessDeniedError("Account is suspended.")


class BannedState(UserState):
    def ensure_access(self, user: "User") -> None:
        raise AccessDeniedError("Account has been banned.")


CURRENT_USER_POLICY_MAP: dict[UserStatusEnum, UserState] = {
    UserStatusEnum.ACTIVE: ActiveState(),
    UserStatusEnum.PENDING: PendingState(),
    UserStatusEnum.SUSPENDED: SuspendedState(),
    UserStatusEnum.BANNED: BannedState(),
}
