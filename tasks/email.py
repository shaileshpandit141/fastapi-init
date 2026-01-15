# pyright: reportUnknownVariableType=false

from smtplib import SMTPException
from typing import Any

from celery.app.task import Task

from celery_app import shared_task
from core.email.base import EmailMessage, build_email_message, send_via_smtp


@shared_task(
    bind=True,
    autoretry_for=(SMTPException,),
    retry_kwargs={"countdown": 60, "max_retries": 3},
)
def send_email_task(self: Task, email_message: dict[str, Any]) -> str:

    email = EmailMessage(**email_message)
    message = build_email_message(email=email)

    try:
        send_via_smtp(message)
    except Exception as exc:
        raise self.retry(exc=exc)  # type: ignore

    return f"Email sent to {email.to}"


class EmailTask:
    @staticmethod
    def send_email(message: EmailMessage) -> None:
        send_email_task.delay(message.model_dump())  # type: ignore
