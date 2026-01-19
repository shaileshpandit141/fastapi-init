from .app_exception import AppException


class ServiceUnavailableException(AppException):
    def __init__(self, service: str = "Service") -> None:
        super().__init__(
            code="SERVICE_UNAVAILABLE",
            message=f"{service} is temporarily unavailable",
            status_code=503,
        )
