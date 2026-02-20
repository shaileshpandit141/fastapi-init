from fastapi import APIRouter

from app.core.config import get_settings

# =============================================================================
# Creating Settings Instance.
# =============================================================================

settings = get_settings()

# =============================================================================
# Creating API Router.
# =============================================================================

router = APIRouter(prefix=settings.app.API_VERSION_PREFIX)
