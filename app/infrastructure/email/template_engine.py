# pyright: reportUnknownVariableType=false

from typing import Any

from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape
from premailer import transform

# =============================================================================
# Email Template Configuration.
# =============================================================================


email_template_env = Environment(
    loader=FileSystemLoader("templates/email"),
    autoescape=select_autoescape(["html", "xml"]),
    undefined=StrictUndefined,
)


# =============================================================================
# Function to Render Email Template.
# =============================================================================


def render_email_template(template_name: str, context: dict[str, Any]) -> str:
    template = email_template_env.get_template(template_name)
    html = template.render(**context)

    return transform(
        html,
        disable_leftover_css=True,
        remove_classes=False,
    )
