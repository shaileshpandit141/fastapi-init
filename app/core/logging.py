from sys import stdout

from .config import get_settings

# =============================================================================
# Creating Settings Instance.
# =============================================================================

settings = get_settings()

# =============================================================================
# Logger Config Dict.
# =============================================================================

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        },
    },
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "stream": stdout,
            "formatter": "default",
        },
    },
    "loggers": {
        "": {
            "handlers": ["default"],
            "level": settings.app.DEBUG,
        },
    },
}
