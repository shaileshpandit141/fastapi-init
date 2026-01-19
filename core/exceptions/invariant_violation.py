from .app_exception import AppException


class InvariantViolationException(AppException):
    def __init__(self, message: str = "System invariant violated") -> None:
        super().__init__(
            code="INVARIANT_VIOLATION",
            message=message,
            status_code=500,
        )
