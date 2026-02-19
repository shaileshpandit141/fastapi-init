from typing import Any

from ..core.exceptions import AppError

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
