from typing import Any

from celery import shared_task


@shared_task(bind=True, max_retries=3)
def send_email_task(self: Any, to_email: str, subject: str, body: str) -> None:
    try:
        # integrate your email service here
        print(f"Sending email to {to_email}")
    except Exception as exc:
        raise self.retry(exc=exc, countdown=5)
