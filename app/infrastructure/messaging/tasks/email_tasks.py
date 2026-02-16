# pyright: reportUnknownVariableType=false

from smtplib import SMTPException
from typing import Any

from celery import shared_task

from ...email.models import EmailMessage
from ...email.service import EmailService

# =============================================================================
# Send Email Task.
# =============================================================================


@shared_task(
    bind=True,
    autoretry_for=(SMTPException,),
    retry_kwargs={"countdown": 60, "max_retries": 3},
)
def send_email_task(self: Any, email_message: dict[str, Any]) -> str:

    email = EmailMessage(**email_message)
    email_service = EmailService()

    try:
        email_service.send(email)
    except Exception as exc:
        raise self.retry(exc=exc)

    return f"Email sent to {email.to}"


# =============================================================================
# Send Email Function.
# =============================================================================


def send_email(message: EmailMessage) -> None:
    send_email_task.delay(message.model_dump())
