from .app_exception import AppHTTPException

# === Resource already exist exception ===


class AlreadyExistsException(AppHTTPException):
    def __init__(self, resource: str = "Resource") -> None:
        super().__init__(
            code="ALREADY_EXISTS",
            message=f"{resource} already exists",
            status_code=409,
        )


# === Bad request exception ===


class BadRequestException(AppHTTPException):
    def __init__(self, message: str) -> None:
        super().__init__(
            code="BAD_REQUEST",
            message=message,
            status_code=400,
        )


# === Resource conflict exception ===


class ConflictException(AppHTTPException):
    def __init__(self, message: str = "Conflict occurred") -> None:
        super().__init__(
            code="CONFLICT",
            message=message,
            status_code=409,
        )


# === Access denied exception ===


class AccessDeniedException(AppHTTPException):
    def __init__(self, message: str = "Access denied") -> None:
        super().__init__(
            code="FORBIDDEN",
            message=message,
            status_code=403,
        )


# === Not found exception ===


class NotFoundException(AppHTTPException):
    def __init__(self, resource: str = "Resource") -> None:
        super().__init__(
            code="NOT_FOUND",
            message=f"{resource} not found",
            status_code=404,
        )


# === Unauthorized exception ===


class UnauthorizedException(AppHTTPException):
    def __init__(self, message: str = "Authentication required") -> None:
        super().__init__(
            code="UNAUTHORIZED",
            message=message,
            status_code=401,
        )
