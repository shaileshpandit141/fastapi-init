import smtplib
from email.mime.multipart import MIMEMultipart

from app.shared.config import get_settings

# =============================================================================
# Gatting Email Env Settings.
# =============================================================================

email_settings = get_settings().email


# =============================================================================
# Function That Send Email Via SMTP.
# =============================================================================


def send_via_smtp(message: MIMEMultipart) -> None:
    with smtplib.SMTP(email_settings.HOST, email_settings.PORT) as server:
        if email_settings.USE_TLS:
            server.starttls()

        if email_settings.USERNAME and email_settings.PASSWORD:
            server.login(
                email_settings.USERNAME,
                email_settings.PASSWORD,
            )

        server.send_message(message)
