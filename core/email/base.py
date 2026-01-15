# pyright: reportUnknownVariableType=false

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any

from pydantic import BaseModel, EmailStr

from core.settings import settings

from .template import render_email_template


class EmailContent(BaseModel):
    html_template: str
    text: str | None = None


class EmailMessage(BaseModel):
    subject: str
    to: EmailStr
    content: EmailContent
    context: dict[str, Any] = {}


def build_email_message(email: EmailMessage) -> MIMEMultipart:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = email.subject
    msg["From"] = settings.email_from
    msg["To"] = email.to

    if email.content.text:
        msg.attach(MIMEText(email.content.text, "plain"))

    html_content = render_email_template(
        template_name=email.content.html_template,
        context={**email.context, "subject": email.subject},
    )
    msg.attach(MIMEText(html_content, "html"))

    return msg


def send_via_smtp(message: MIMEMultipart) -> None:
    with smtplib.SMTP(settings.email_host, settings.email_port) as server:
        server.starttls()
        server.login(settings.email_user, settings.email_password)
        server.send_message(message)
