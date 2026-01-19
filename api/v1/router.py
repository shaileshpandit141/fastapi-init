from fastapi import APIRouter

from .endpoints import auth, health, users

router = APIRouter(prefix="/v1")

# === Include all router endpoints ===


router.include_router(health.router)
router.include_router(auth.router)
router.include_router(users.router)
