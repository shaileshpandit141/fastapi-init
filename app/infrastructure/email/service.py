from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.shared.config import get_settings

from .models import EmailMessage
from .template_engine import render_email_template
from .smtp_client import send_via_smtp


settings = get_settings()


class EmailService:
    def build_message(self, email: EmailMessage) -> MIMEMultipart:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = email.subject
        msg["From"] = settings.email.FROM_EMAIL
        msg["To"] = email.to

        if email.content.text:
            msg.attach(MIMEText(email.content.text, "plain"))

        html_content = render_email_template(
            template_name=email.content.html_template,
            context={**email.context, "subject": email.subject},
        )

        msg.attach(MIMEText(html_content, "html"))
        return msg

    def send(self, email: EmailMessage) -> None:
        message = self.build_message(email)
        send_via_smtp(message)
