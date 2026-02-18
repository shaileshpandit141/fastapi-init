from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.shared.config import get_settings

from .renderer import BaseRenderer
from .types import EmailMessageDict

# =============================================================================
# Gatting Env Settings.
# =============================================================================

settings = get_settings()


# =============================================================================
# SMTP Message Assembler Class.
# =============================================================================


class SmtpMessageAssembler:
    def __init__(self, renderer: BaseRenderer) -> None:
        self._from_email = settings.email.FROM_EMAIL
        self._renderer = renderer

    def assemble(self, email_msg: EmailMessageDict) -> MIMEMultipart:
        message = MIMEMultipart("alternative")
        message["Subject"] = email_msg["subject"]
        message["From"] = self._from_email
        message["To"] = email_msg["to"]

        text = email_msg["content"].get("text")

        if text:
            message.attach(MIMEText(text, "plain"))

        html = self._renderer.render(
            template=email_msg["content"]["html_template"],
            context={
                **email_msg["context"],
                "subject": email_msg["subject"],
            },
        )
        message.attach(MIMEText(html, "html"))

        return message
