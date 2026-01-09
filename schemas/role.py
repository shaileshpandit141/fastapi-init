from sqlmodel import Field

from models.role import RoleBase
from schemas.base import NonEmptyUpdateModel


class RoleRead(RoleBase):
    pass


class RoleCreate(RoleBase):
    pass


class RoleUpdate(NonEmptyUpdateModel):
    name: str | None = Field(default=None, max_length=50)
    description: str | None = Field(default=None, max_length=255)
