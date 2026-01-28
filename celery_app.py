# pyright: reportUnknownMemberType=false, reportUnknownVariableType=false

from typing import Any, Callable, cast

from celery import Celery  # type: ignore
from celery.local import PromiseProxy, Proxy

from core.settings import settings

celery = Celery(
    "fastapi-init",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["tasks"],
)

celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    worker_max_tasks_per_child=100,
)


def shared_task(
    *,
    bind: bool = False,
    name: str | None = None,
    max_retries: int | None = None,
    default_retry_delay: int | None = None,
    autoretry_for: tuple[type[Exception], ...] = (),
    retry_kwargs: dict[str, Any],
    **kwargs: Any,
) -> PromiseProxy:
    """Type-safe shared_task decorator for Celery."""

    def wrapper(func: PromiseProxy) -> Proxy | Callable[..., Proxy] | PromiseProxy:
        return celery.task(
            func,
            bind=bind,
            name=name,
            max_retries=max_retries,
            default_retry_delay=default_retry_delay,
            autoretry_for=autoretry_for,
            retry_kwargs=retry_kwargs,
            **kwargs,
        )

    return cast(PromiseProxy, wrapper)
