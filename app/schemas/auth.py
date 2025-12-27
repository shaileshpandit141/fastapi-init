from sqlmodel import SQLModel


# --- Pydantic I/O schema ---


class TokenRead(SQLModel):
    access_token: str
    refresh_token: str
    token_type: str
