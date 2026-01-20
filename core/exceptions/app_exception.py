from core.response.schemas import ErrorDetailDict

# === A global app exception ===


class AppException(Exception):
    def __init__(self, *, detail: str | list[ErrorDetailDict]) -> None:
        super().__init__(detail)
        self.detail = detail


# ===  Root App http exception ===


class AppHTTPException(AppException):
    def __init__(
        self,
        *,
        detail: str | list[ErrorDetailDict],
        status_code: int,
    ) -> None:
        super().__init__(detail=detail)
        self.status_code = status_code
