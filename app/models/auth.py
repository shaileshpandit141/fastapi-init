from sqlmodel import SQLModel


# --- I/O schema ---


class TokenRead(SQLModel):
    access_token: str
    token_type: str
