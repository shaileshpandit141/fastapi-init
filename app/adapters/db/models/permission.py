from typing import TYPE_CHECKING

from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel

from ._mixins import UUIDv7Mixin

if TYPE_CHECKING:
    from .role import Role

# =============================================================================
# Permission Base SQLModel.
# =============================================================================


class PermissionBase(SQLModel, table=False):
    code: str = Field(
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
# Permission SQLModel.
# =============================================================================


class Permission(PermissionBase, UUIDv7Mixin, table=True):
    __tablename__ = "permissions"  # type: ignore

    roles: list["Role"] = Relationship(back_populates="permission")
