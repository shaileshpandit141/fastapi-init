from dataclasses import dataclass


@dataclass(slots=True)
class RefreshTokenCommand:
    token: str
