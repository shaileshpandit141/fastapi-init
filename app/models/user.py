from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: None | int = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    is_active: bool = Field(default=True)
