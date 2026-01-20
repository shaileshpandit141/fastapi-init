from typing import Any

from core.response.schemas import ErrorResponse

OpenAPIResponses = dict[int | str, dict[str, Any]]

SYSTEM_ERRORS: OpenAPIResponses = {
    500: {"model": ErrorResponse, "description": "Internal server error"},
}

VALIDATION_ERRORS: OpenAPIResponses = {
    422: {"model": ErrorResponse, "description": "Validation error"},
}

AUTH_ERRORS: OpenAPIResponses = {
    401: {"model": ErrorResponse, "description": "Unauthorized"},
}

PERMISSION_ERRORS: OpenAPIResponses = {
    403: {"model": ErrorResponse, "description": "Forbidden"},
}

READ_ERRORS: OpenAPIResponses = {
    404: {"model": ErrorResponse, "description": "Resource not found"},
}

WRITE_ERRORS: OpenAPIResponses = {
    400: {"model": ErrorResponse, "description": "Bad request"},
    409: {"model": ErrorResponse, "description": "Conflict"},
}

RATE_LIMIT_ERRORS: OpenAPIResponses = {
    429: {"model": ErrorResponse, "description": "Too many requests"},
}

PUBLIC_READ: OpenAPIResponses = {
    **READ_ERRORS,
    **VALIDATION_ERRORS,
    **RATE_LIMIT_ERRORS,
    **SYSTEM_ERRORS,
}

PUBLIC_WRITE: OpenAPIResponses = {
    **WRITE_ERRORS,
    **VALIDATION_ERRORS,
    **RATE_LIMIT_ERRORS,
    **SYSTEM_ERRORS,
}

AUTH_READ: OpenAPIResponses = {
    **AUTH_ERRORS,
    **READ_ERRORS,
    **VALIDATION_ERRORS,
    **SYSTEM_ERRORS,
}

AUTH_WRITE: OpenAPIResponses = {
    **AUTH_ERRORS,
    **WRITE_ERRORS,
    **VALIDATION_ERRORS,
    **SYSTEM_ERRORS,
}

ADMIN_WRITE: OpenAPIResponses = {
    **AUTH_ERRORS,
    **PERMISSION_ERRORS,
    **WRITE_ERRORS,
    **VALIDATION_ERRORS,
    **SYSTEM_ERRORS,
}
