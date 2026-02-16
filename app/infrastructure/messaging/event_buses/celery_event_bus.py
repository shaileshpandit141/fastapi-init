from typing import Any

from celery import Celery

# =============================================================================
# Defining Celery Event Bus.
# =============================================================================


class CeleryEventBus:
    def __init__(self, celery_app: Celery) -> None:
        self.celery_app = celery_app

    def publish(self, task_name: str, payload: dict[str, Any]) -> None:
        self.celery_app.send_task(task_name, kwargs=payload)
