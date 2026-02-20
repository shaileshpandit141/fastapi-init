from typing import Any

from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel

from ._mixins import UUIDv7Mixin

# =============================================================================
# Role Base SQLModel.
# =============================================================================


class RoleBase(SQLModel, table=False):
    name: str = Field(
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

    users: list[Any] = Relationship(back_populates="role")
    permissions: list[Any] = Relationship(back_populates="role")
