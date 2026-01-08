from sqlmodel import SQLModel


class MessageRead(SQLModel):
    detail: str
