from .app_exception import AppException


class NotFoundException(AppException):
    def __init__(self, resource: str = "Resource") -> None:
        super().__init__(
            code="NOT_FOUND",
            message=f"{resource} not found",
            status_code=404,
        )
