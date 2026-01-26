from typing import Any, TypedDict

OpenAPIResponses = dict[int | str, dict[str, Any]]


class SwaggerConfigDict(TypedDict, total=False):
    summary: str
    description: str
    responses: dict[int | str, dict[str, Any]]
