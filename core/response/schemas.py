from typing import Any

from sqlmodel import SQLModel


class DetailResponse(SQLModel):
    detail: str


class ErrorPayload(SQLModel):
    code: str
    message: str
    details: list[dict[str, Any]] = []


class ErrorResponse(SQLModel):
    error: ErrorPayload
