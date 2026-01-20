from typing import Any

# === A global app exception ===


class AppException(Exception):
    def __init__(
        self,
        *,
        code: str,
        message: str,
        details: list[dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details or []


# ===  Root App http exception ===


class AppHTTPException(AppException):
    def __init__(
        self,
        *,
        code: str,
        message: str,
        status_code: int,
        details: list[dict[str, Any]] | None = None,
    ) -> None:
        self.status_code = status_code
        super().__init__(code=code, message=message, details=details)
