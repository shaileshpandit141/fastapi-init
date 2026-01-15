# pyright: reportUnknownVariableType=false

from typing import Any

from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape
from premailer import transform

email_template_env = Environment(
    loader=FileSystemLoader("templates/email"),
    autoescape=select_autoescape(["html", "xml"]),
    undefined=StrictUndefined,
)


def render_email_template(template_name: str, context: dict[str, Any]) -> str:
    template = email_template_env.get_template(template_name)
    html = template.render(**context)

    # Inline CSS (styles.css)
    html = transform(
        html,
        disable_leftover_css=True,
        remove_classes=False,
    )

    return html
