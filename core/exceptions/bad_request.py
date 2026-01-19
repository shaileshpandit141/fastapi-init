from .app_exception import AppException


class BadRequestException(AppException):
    def __init__(self, message: str) -> None:
        super().__init__(
            code="BAD_REQUEST",
            message=message,
            status_code=400,
        )
