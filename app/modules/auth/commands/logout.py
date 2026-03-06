from dataclasses import dataclass


@dataclass(slots=True)
class LogoutCommand:
    access_token: str
    refresh_token: str
