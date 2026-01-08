from sqlmodel import Field, SQLModel


class RoleRead(SQLModel):
    id: int
    name: str
    description: str | None = None


class RoleCreate(SQLModel):
    name: str
    description: str | None = None


class PermissionCreate(SQLModel):
    code: str
    description: str | None = Field(default=None, max_length=255)
