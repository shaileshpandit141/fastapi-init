from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape



class BaseRenderer:
    def __init__(self) -> None:
        self._env = Environment(
            loader=FileSystemLoader("templates/email"),
            autoescape=select_autoescape(["html", "xml"]),
            undefined=StrictUndefined,
        )

    def render(self, template: str, context: dict[str, str]) -> str:
        raise NotImplementedError


class JinjaRenderer(BaseRenderer):
    def render(self, template: str, context: dict[str, str]) -> str:
        template_obj = self._env.get_template(template)
        return template_obj.render(**context)
