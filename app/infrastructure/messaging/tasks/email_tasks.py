# pyright: reportUnknownVariableType=false

from logging import getLogger
from smtplib import SMTPException
from typing import Any

from celery import shared_task

from app.infrastructure.email.assembler import EmailMessageDict, SmtpMessageAssembler
from app.infrastructure.email.renderer import JinjaRenderer
from app.infrastructure.email.smtp_client import SmtpEmailClient

# =============================================================================
# Getting Logger.
# =============================================================================

logger = getLogger(__name__)


# =============================================================================
# Celery Send Email Task.
# =============================================================================


@shared_task(
    bind=True,
    autoretry_for=(SMTPException,),
    retry_kwargs={"countdown": 60, "max_retries": 3},
    retry_backoff=True,
    retry_jitter=True,
    ignore_result=True,
)
def send_email_task(self: Any, email_msg: EmailMessageDict) -> None:
    assembler = SmtpMessageAssembler(JinjaRenderer())
    message = assembler.assemble(email_msg)
    email_client = SmtpEmailClient()

    try:
        email_client.send(message)
        logger.info(
            "Email successfully sent",
            extra={
                "to": email_msg["to"],
                "subject": email_msg["subject"],
            },
        )
    except SMTPException as exc:
        logger.warning(
            "SMTP error while sending email. Retrying...",
            extra={"to": email_msg["to"]},
            exc_info=exc,
        )
        raise self.retry(exc=exc)
    except Exception as exc:
        logger.exception(
            "Unexpected error while sending email",
            extra={"to": email_msg["to"]},
            exc_info=exc,
        )
