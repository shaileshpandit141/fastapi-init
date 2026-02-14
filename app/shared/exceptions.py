from typing import Any

# =============================================================================
# Root app error (used globaly)
# =============================================================================


class AppError(Exception):
    def __init__(self, detail: str | list[Any]) -> None:
        super().__init__(detail)
        self.detail = detail


# =============================================================================
# Unit Of Work Error
# =============================================================================


class UnitOfWorkError(AppError):
    pass
