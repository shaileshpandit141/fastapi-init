from slowapi import Limiter
from slowapi.util import get_remote_address

from core.config.settings import settings

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100/minute"],
    storage_uri=settings.redis_url,
    headers_enabled=True,
)
