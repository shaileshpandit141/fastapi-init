from fastapi import APIRouter

from .endpoints import auth, health

router = APIRouter(prefix="/v1")

router.include_router(health.router)
router.include_router(auth.router)
