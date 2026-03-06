from fastapi import APIRouter

from app.core.config import get_settings

from .routers import auth
from .routers import user

# =============================================================================
# Creating Settings Instance.
# =============================================================================

settings = get_settings()

# =============================================================================
# Creating API Router.
# =============================================================================

router = APIRouter(prefix=settings.app.API_VERSION_PREFIX)
router.include_router(auth.router)
router.include_router(user.router)
