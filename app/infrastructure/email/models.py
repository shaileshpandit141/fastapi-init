from typing import Any

from pydantic import BaseModel, EmailStr

# =============================================================================
# Email Content Model.
# =============================================================================


class EmailContent(BaseModel):
    html_template: str
    text: str | None = None


# =============================================================================
# Email Message Content Model.
# =============================================================================


class EmailMessage(BaseModel):
    subject: str
    to: EmailStr
    content: EmailContent
    context: dict[str, Any] = {}
