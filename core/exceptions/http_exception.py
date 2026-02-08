from core.response.schemas import ErrorDetailDict

from .app_exception import AppError

# =============================================================================
# Root http error
# =============================================================================


class HTTPError(AppError):
    def __init__(self, detail: str | list[ErrorDetailDict], status_code: int) -> None:
        super().__init__(detail=detail)
        self.status_code = status_code


# =============================================================================
# Bad request error
# =============================================================================


class BadRequestError(HTTPError):
    def __init__(self, detail: str | list[ErrorDetailDict]) -> None:
        super().__init__(detail=detail, status_code=400)


# =============================================================================
# Unauthorized error
# =============================================================================


class UnauthorizedError(HTTPError):
    def __init__(self, detail: str | list[ErrorDetailDict]) -> None:
        super().__init__(detail=detail, status_code=401)


# =============================================================================
# Access denied error
# =============================================================================


class AccessDeniedError(HTTPError):
    def __init__(self, detail: str | list[ErrorDetailDict]) -> None:
        super().__init__(detail=detail, status_code=403)


# =============================================================================
# Not found error
# =============================================================================


class NotFoundError(HTTPError):
    def __init__(self, detail: str | list[ErrorDetailDict]) -> None:
        super().__init__(detail=detail, status_code=404)


# =============================================================================
# Resource already exist error
# =============================================================================


class AlreadyExistsError(HTTPError):
    def __init__(self, detail: str | list[ErrorDetailDict]) -> None:
        super().__init__(detail=detail, status_code=409)
