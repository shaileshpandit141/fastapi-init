from enum import StrEnum
from typing import Callable

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.shared.config import get_settings

# =============================================================================
# Getting All Env Settings.
# =============================================================================

settings = get_settings()


# =============================================================================
# Rate Limits Enum.
# =============================================================================


class RateLimit(StrEnum):
    LOGIN = "5/minute"
    REGISTER = "3/minute"
    DEFAULT = "100/minute"


# =============================================================================
# Creating Slowapi Limiter Instance.
# =============================================================================

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=settings.redis.url,
    strategy="fixed-window",
    default_limits=[RateLimit.DEFAULT.value],
    headers_enabled=True,
)


# =============================================================================
# Decorator Fun Return Type.
# =============================================================================

type FunType = Callable[..., object]


# =============================================================================
# Type-safe Decorator Function.
# =============================================================================


def rate_limit(limit: RateLimit) -> Callable[[FunType], FunType]:
    def decorator(func: FunType) -> FunType:
        return limiter.limit(limit.value)(func)  # type: ignore

    return decorator
