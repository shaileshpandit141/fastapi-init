from typing import Any

from sqlmodel import SQLModel

OpenAPIResponses = dict[int | str, dict[str, Any]]


class DetailResponse(SQLModel):
    detail: str
