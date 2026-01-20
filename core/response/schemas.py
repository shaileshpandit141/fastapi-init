from typing import Any

from sqlmodel import SQLModel

OpenAPIResponses = dict[int | str, dict[str, Any]]


class DetailResponse(SQLModel):
    detail: str


class ErrorPayload(SQLModel):
    code: str
    message: str
    details: list[dict[str, Any]] = []


class ErrorResponse(SQLModel):
    error: ErrorPayload
