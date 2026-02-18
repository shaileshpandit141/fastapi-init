from typing import Any, TypedDict

# =============================================================================
# Email Content Model.
# =============================================================================


class TextContent(TypedDict, total=False):
    text: str


class EmailContentDict(TextContent):
    html_template: str


# =============================================================================
# Email Message Content Model.
# =============================================================================


class EmailMessageDict(TypedDict):
    subject: str
    to: str
    content: EmailContentDict
    context: dict[str, Any]


def send_email(message: EmailMessageDict) -> EmailMessageDict:
    return message


send_email(
    {
        "subject": "This is email subject.",
        "to": "client@gmail.com",
        "content": {
            "html_template": "",
        },
        "context": {},
    }
)
