from celery import Celery

from app.shared.config import get_settings

# =============================================================================
# Gatting Env Celery Settings.
# =============================================================================

celery_settings = get_settings().celery


# =============================================================================
# Creating Celery App Instance.
# =============================================================================


celery_app = Celery(
    main="app",
    broker=celery_settings.BROKER_URL,
    backend=celery_settings.RESULT_BACKEND,
)

celery_app.conf.task_always_eager = True
celery_app.conf.task_eager_propagates = True

# =============================================================================
# Updating Celery Config With My Config.
# =============================================================================


celery_app.conf.update(
    task_serializer=celery_settings.TASK_SERIALIZER,
    result_serializer=celery_settings.RESULT_SERIALIZER,
    accept_content=celery_settings.ACCEPT_CONTENT,
    timezone=celery_settings.TIMEZONE,
    enable_utc=celery_settings.ENABLE_UTC,
)


# =============================================================================
# Auto-Discover Celery Tasks.
# =============================================================================


celery_app.autodiscover_tasks(
    packages=["app.infrastructure.messaging.tasks"],
)
