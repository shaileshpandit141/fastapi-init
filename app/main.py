from logging.config import dictConfig

from fastapi import FastAPI

from .shared.config import get_settings
from .shared.exc_handlers import register_exception_handlers
from .shared.lifespan import lifespan
from .shared.logging import LOGGING_CONFIG
from .shared.middleware import include_middlewares

# =============================================================================
# Creating Settings Instance.
# =============================================================================

settings = get_settings()

# =============================================================================
# Setup Local Logger.
# =============================================================================

dictConfig(LOGGING_CONFIG)

# =============================================================================
# Creating FastAPI App Instance.
# =============================================================================

app = FastAPI(
    title=settings.app.NAME,
    debug=settings.app.DEBUG,
    lifespan=lifespan,
)

# =============================================================================
# Register Custom Exception Handlers.
# =============================================================================

register_exception_handlers(app)

# =============================================================================
# Include all middlewares
# =============================================================================

include_middlewares(app)
