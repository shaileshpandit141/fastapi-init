from typing import Any


class AppError(Exception):
    def __init__(
        self, *, code: int | str, detail: str, extra: dict[str, Any] | None = None
    ) -> None:
        self.code = code
        self.detail = detail
        self.extra = extra or {}
        super().__init__(detail)
