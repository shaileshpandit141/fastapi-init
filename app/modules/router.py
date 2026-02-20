from fastapi import APIRouter

from app.core.config import get_settings

from .auth.routes import router as auth_router

# =============================================================================
# Creating Settings Instance.
# =============================================================================

settings = get_settings()

# =============================================================================
# Creating API Router.
# =============================================================================

router = APIRouter(prefix=settings.app.API_VERSION_PREFIX)
router.include_router(auth_router)
