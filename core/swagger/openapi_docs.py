from .constants import (
    ACCESS_MAP,
    DESCRIPTION_MAP,
    RESPONSE_KEY_MAP,
    SUMMARY_MAP,
    Access,
    Action,
)
from .responses import RESPONSE_MAP
from .types import SwaggerConfigDict


def openapi_docs(*, action: Action, resource: str, access: Access) -> SwaggerConfigDict:
    """
    Build FastAPI-compatible Swagger metadata.
    """
    name = resource.lower()

    return {
        "summary": SUMMARY_MAP[action].format(resource=resource),
        "description": (
            f"{DESCRIPTION_MAP[action].format(name=name)} " f"{ACCESS_MAP[access]}"
        ),
        "responses": RESPONSE_MAP[RESPONSE_KEY_MAP[(action, access)]],
    }
