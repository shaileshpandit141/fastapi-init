from dataclasses import dataclass


@dataclass(slots=True)
class LoginCommand:
    email: str
    password: str
