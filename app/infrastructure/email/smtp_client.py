import smtplib
from email.mime.multipart import MIMEMultipart

from app.core.config import get_settings

# =============================================================================
# Gatting Env Settings.
# =============================================================================

settings = get_settings()

# =============================================================================
# Smtp Email Client For Sending The HTML Email.
# =============================================================================


class SmtpEmailClient:
    def send(self, message: MIMEMultipart) -> None:
        with smtplib.SMTP(settings.email.HOST, settings.email.PORT) as server:
            if settings.email.USE_TLS:
                server.starttls()

            if settings.email.USERNAME and settings.email.PASSWORD:
                server.login(settings.email.USERNAME, settings.email.PASSWORD)

            server.send_message(message)
