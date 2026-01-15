from sqlmodel import Field  # type: ignore

from core.db.base import BaseIntIDModel, NonEmptyUpdateModel

from .models import PermissionBase, RoleBase, RolePermissionBase, UserRoleBase

# === Role Schemas ===


class RoleRead(RoleBase):
    pass


class RoleCreate(RoleBase):
    pass


class RoleUpdate(NonEmptyUpdateModel):
    name: str | None = Field(default=None, max_length=50)
    description: str | None = Field(default=None, max_length=255)


# === Permission Schemas ===


class PermissionRead(PermissionBase, BaseIntIDModel):
    pass


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(NonEmptyUpdateModel):
    code: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=255)


# === Role Permission Schemas ===


class RolePermissionRead(RolePermissionBase):
    pass


class RolePermissionCreate(RolePermissionBase):
    pass


class RolePermissionUpdate(NonEmptyUpdateModel):
    role_id: int | None = None
    permission_id: int | None = None


# === Uer Role Schemas ===


class UserRoleRead(UserRoleBase):
    pass


class UserRoleCreate(UserRoleBase):
    pass


class UserRoleUpdate(NonEmptyUpdateModel):
    user_id: int | None = None
    role_id: int | None = None
