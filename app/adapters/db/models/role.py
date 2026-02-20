from typing import TYPE_CHECKING

from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel

from app.shared.enums.role import RoleEnum

from ._mixins import UUIDv7Mixin

if TYPE_CHECKING:
    from .permission import Permission
    from .user import User

# =============================================================================
# Role Base SQLModel.
# =============================================================================


class RoleBase(SQLModel, table=False):
    name: RoleEnum = Field(
        max_length=50,
        sa_column=Column(
            String(50),
            unique=True,
            index=True,
            nullable=False,
        ),
    )
    description: str | None = Field(
        default=None,
        max_length=255,
        sa_column=Column(
            String(255),
        ),
    )


# =============================================================================
# Role SQLModel.
# =============================================================================


class Role(RoleBase, UUIDv7Mixin, table=True):
    __tablename__ = "roles"  # type: ignore

    users: list["User"] = Relationship(back_populates="role")
    permissions: list["Permission"] = Relationship(back_populates="role")
