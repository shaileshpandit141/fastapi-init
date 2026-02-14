from logging.config import dictConfig

from fastapi import FastAPI

from .shared.config import get_settings
from .shared.lifespan import lifespan
from .shared.logging import LOGGING_CONFIG

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
    title=settings.app.APP_NAME,
    debug=settings.app.DEBUG,
    lifespan=lifespan,
)
