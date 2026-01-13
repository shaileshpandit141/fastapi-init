from celery import Celery

from core.settings import settings

celery_app = Celery("tasks")

celery_app.conf.update(  # type: ignore[attr-defined]
    broker_url=settings.celery_broker_url,
    result_backend=settings.celery_broker_url,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)
