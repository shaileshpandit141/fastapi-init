from .app_exception import AppException


class ForbiddenException(AppException):
    def __init__(self, message: str = "Access denied") -> None:
        super().__init__(
            code="FORBIDDEN",
            message=message,
            status_code=403,
        )
