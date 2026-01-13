from sqlmodel import SQLModel


class DetailResponse(SQLModel):
    detail: str
