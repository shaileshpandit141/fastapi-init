from core.response.schemas import ErrorDetailDict

from .app_exception import AppHTTPException

# === Bad request exception ===


class BadRequestException(AppHTTPException):
    def __init__(self, *, detail: str | list[ErrorDetailDict]) -> None:
        super().__init__(detail=detail, status_code=400)


# === Unauthorized exception ===


class UnauthorizedException(AppHTTPException):
    def __init__(self, *, detail: str | list[ErrorDetailDict]) -> None:
        super().__init__(detail=detail, status_code=401)


# === Access denied exception ===


class AccessDeniedException(AppHTTPException):
    def __init__(self, *, detail: str | list[ErrorDetailDict]) -> None:
        super().__init__(detail=detail, status_code=403)


# === Not found exception ===


class NotFoundException(AppHTTPException):
    def __init__(self, *, detail: str | list[ErrorDetailDict]) -> None:
        super().__init__(detail=detail, status_code=404)


# === Resource already exist exception ===


class AlreadyExistsException(AppHTTPException):
    def __init__(self, *, detail: str | list[ErrorDetailDict]) -> None:
        super().__init__(detail=detail, status_code=409)
