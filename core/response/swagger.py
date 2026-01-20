from typing import Any

from core.response.schemas import DetailResponse, ErrorResponse

OpenAPIResponses = dict[int | str, dict[str, Any]]

NO_CONTENT_ERROR: OpenAPIResponses = {
    204: {
        "model": None,
        "description": "No content found.",
    }
}

VALIDATION_ERRORS: OpenAPIResponses = {
    422: {
        "model": ErrorResponse,
        "description": "Validation error.",
    }
}

AUTH_ERRORS: OpenAPIResponses = {
    401: {
        "model": DetailResponse,
        "description": "Unauthorized.",
    }
}

PERMISSION_ERRORS: OpenAPIResponses = {
    403: {
        "model": DetailResponse,
        "description": "Forbidden.",
    }
}

READ_ERRORS: OpenAPIResponses = {
    404: {
        "model": DetailResponse,
        "description": "Resource not found.",
    }
}

WRITE_ERRORS: OpenAPIResponses = {
    400: {
        "model": DetailResponse,
        "description": "Bad request.",
    },
    409: {
        "model": DetailResponse,
        "description": "Resource already exists.",
    },
}

RATE_LIMIT_ERRORS: OpenAPIResponses = {
    429: {
        "model": DetailResponse,
        "description": "Too many requests.",
    }
}

SYSTEM_ERRORS: OpenAPIResponses = {
    500: {
        "model": DetailResponse,
        "description": "Internal server error.",
    }
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
    **PERMISSION_ERRORS,
    **READ_ERRORS,
    **VALIDATION_ERRORS,
    **SYSTEM_ERRORS,
}

AUTH_WRITE: OpenAPIResponses = {
    **AUTH_ERRORS,
    **PERMISSION_ERRORS,
    **WRITE_ERRORS,
    **VALIDATION_ERRORS,
    **SYSTEM_ERRORS,
}

ADMIN_READ: OpenAPIResponses = {
    **AUTH_ERRORS,
    **PERMISSION_ERRORS,
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

DELETE_RECORD: OpenAPIResponses = {
    **AUTH_ERRORS,
    **PERMISSION_ERRORS,
    **VALIDATION_ERRORS,
    **NO_CONTENT_ERROR,
    **SYSTEM_ERRORS,
}
