from .app_exception import AppException


class AlreadyExistsException(AppException):
    def __init__(self, resource: str = "Resource") -> None:
        super().__init__(
            code="ALREADY_EXISTS",
            message=f"{resource} already exists",
            status_code=409,
        )
