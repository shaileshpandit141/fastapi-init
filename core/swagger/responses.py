from typing import Any

from core.response.schemas import DetailResponse, ErrorResponse

from .constants import ResponseSpec

OpenAPIResponses = dict[int | str, dict[str, Any]]


# ---- base error blocks ----

NO_CONTENT_ERROR: OpenAPIResponses = {
    204: {"model": None, "description": "No content."}
}

VALIDATION_ERRORS: OpenAPIResponses = {
    422: {"model": ErrorResponse, "description": "Validation error."}
}

AUTH_ERRORS: OpenAPIResponses = {
    401: {"model": DetailResponse, "description": "Unauthorized."}
}

PERMISSION_ERRORS: OpenAPIResponses = {
    403: {"model": DetailResponse, "description": "Forbidden."}
}

READ_ERRORS: OpenAPIResponses = {
    404: {"model": DetailResponse, "description": "Resource not found."}
}

WRITE_ERRORS: OpenAPIResponses = {
    400: {"model": DetailResponse, "description": "Bad request."},
    409: {"model": DetailResponse, "description": "Resource already exists."},
}

RATE_LIMIT_ERRORS: OpenAPIResponses = {
    429: {"model": DetailResponse, "description": "Too many requests."}
}

SYSTEM_ERRORS: OpenAPIResponses = {
    500: {"model": DetailResponse, "description": "Internal server error."}
}


# ---- response profiles ----

RESPONSE_MAP: dict[ResponseSpec, OpenAPIResponses] = {
    ResponseSpec.PUBLIC_READ: {
        **READ_ERRORS,
        **VALIDATION_ERRORS,
        **RATE_LIMIT_ERRORS,
        **SYSTEM_ERRORS,
    },
    ResponseSpec.PUBLIC_WRITE: {
        **WRITE_ERRORS,
        **VALIDATION_ERRORS,
        **RATE_LIMIT_ERRORS,
        **SYSTEM_ERRORS,
    },
    ResponseSpec.AUTHENTICATED_READ: {
        **AUTH_ERRORS,
        **PERMISSION_ERRORS,
        **READ_ERRORS,
        **VALIDATION_ERRORS,
        **SYSTEM_ERRORS,
    },
    ResponseSpec.AUTHENTICATED_WRITE: {
        **AUTH_ERRORS,
        **PERMISSION_ERRORS,
        **WRITE_ERRORS,
        **VALIDATION_ERRORS,
        **SYSTEM_ERRORS,
    },
    ResponseSpec.AUTHENTICATED_DELETE: {
        **AUTH_ERRORS,
        **PERMISSION_ERRORS,
        **VALIDATION_ERRORS,
        **NO_CONTENT_ERROR,
        **SYSTEM_ERRORS,
    },
}

PUBLIC_WRITE = RESPONSE_MAP[ResponseSpec.PUBLIC_WRITE]
PUBLIC_READ = RESPONSE_MAP[ResponseSpec.PUBLIC_READ]

AUTH_WRITE = RESPONSE_MAP[ResponseSpec.AUTHENTICATED_WRITE]
AUTH_READ = RESPONSE_MAP[ResponseSpec.AUTHENTICATED_READ]
AUTH_DELETE = RESPONSE_MAP[ResponseSpec.AUTHENTICATED_DELETE]
