from .app_exception import AppException


class ConflictException(AppException):
    def __init__(self, message: str = "Conflict occurred") -> None:
        super().__init__(
            code="CONFLICT",
            message=message,
            status_code=409,
        )
