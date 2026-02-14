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


# =============================================================================
# Root http error
# =============================================================================


class HTTPError(AppError):
    def __init__(self, detail: str | list[Any], status_code: int) -> None:
        super().__init__(detail=detail)
        self.status_code = status_code
