from typing import Any

from .types import ErrorDetailDict

# =============================================================================
# Root app error (used globaly)
# =============================================================================


class AppError(Exception):
    def __init__(self, detail: str | list[Any]) -> None:
        super().__init__(detail)
        self.detail = detail


# =============================================================================
# Root Http Error.
# =============================================================================


class HTTPError(AppError):
    def __init__(self, detail: str | list[Any], status_code: int) -> None:
        super().__init__(detail=detail)
        self.status_code = status_code


# =============================================================================
# Bad Request Error.
# =============================================================================


class BadRequestError(HTTPError):
    def __init__(self, detail: str | list[ErrorDetailDict]) -> None:
        super().__init__(detail=detail, status_code=400)


# =============================================================================
# Unauthorized Error.
# =============================================================================


class UnauthorizedError(HTTPError):
    def __init__(self, detail: str | list[ErrorDetailDict]) -> None:
        super().__init__(detail=detail, status_code=401)


# =============================================================================
# Access Denied Error.
# =============================================================================


class AccessDeniedError(HTTPError):
    def __init__(self, detail: str | list[ErrorDetailDict]) -> None:
        super().__init__(detail=detail, status_code=403)


# =============================================================================
# Not Found Error.
# =============================================================================


class NotFoundError(HTTPError):
    def __init__(self, detail: str | list[ErrorDetailDict]) -> None:
        super().__init__(detail=detail, status_code=404)


# =============================================================================
# Resource Already Exist Error.
# =============================================================================


class AlreadyExistsError(HTTPError):
    def __init__(self, detail: str | list[ErrorDetailDict]) -> None:
        super().__init__(detail=detail, status_code=409)
