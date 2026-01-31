from typing import Callable

from slowapi import Limiter
from slowapi.util import get_remote_address

from core.settings import settings

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100/minute"],
    storage_uri=settings.redis_url or "memory://",
    headers_enabled=True,
    retry_after="http-date",
)


def limit[T: Callable[..., object]](limit: object) -> Callable[[T], T]:
    def decorator(func: T) -> T:
        return limiter.limit(limit)(func)  # type: ignore

    return decorator
