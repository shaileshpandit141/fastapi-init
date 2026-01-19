from .app_exception import AppException


class TimeoutException(AppException):
    def __init__(self):
        super().__init__(
            code="TIMEOUT",
            message="Operation timed out",
            status_code=504,
        )
