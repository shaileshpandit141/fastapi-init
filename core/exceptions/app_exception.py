from core.response.schemas import ErrorDetailDict

# =============================================================================
# Root app error (used glogely)
# =============================================================================


class AppError(Exception):
    def __init__(self, detail: str | list[ErrorDetailDict]) -> None:
        super().__init__(detail)
        self.detail = detail
