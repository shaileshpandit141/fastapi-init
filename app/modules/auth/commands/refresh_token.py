from dataclasses import dataclass


@dataclass(slots=True)
class RefreshTokenCommand:
    refresh_token: str
