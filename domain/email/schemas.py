from typing import Any

from pydantic import BaseModel, EmailStr


class EmailContent(BaseModel):
    html_template: str
    text: str | None = None


class EmailMessage(BaseModel):
    subject: str
    to: EmailStr
    content: EmailContent
    context: dict[str, Any] = {}
