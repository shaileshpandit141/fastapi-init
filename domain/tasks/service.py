from domain.email.schemas import EmailMessage

from .email import send_email_task


class EmailService:
    @staticmethod
    def send_email(message: EmailMessage) -> None:
        send_email_task.delay(**message.model_dump())  # type: ignore
