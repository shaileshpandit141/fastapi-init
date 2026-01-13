# pyright: reportUnknownVariableType=false

from smtplib import SMTPException

from celery import shared_task
from celery.app.task import Task

from domain.email.schemas import EmailMessage
from domain.email.service import build_email_message, send_via_smtp


@shared_task(
    bind=True,
    autoretry_for=(SMTPException,),
    retry_kwargs={"countdown": 60, "max_retries": 3},
)
def send_email_task(self: Task, email_message: EmailMessage) -> str:
    message = build_email_message(email_message)

    try:
        send_via_smtp(message)
    except Exception as exc:
        raise self.retry(exc=exc)  # type: ignore

    return f"Email sent to {email_message.to}"
