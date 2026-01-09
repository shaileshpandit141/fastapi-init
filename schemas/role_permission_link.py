from models.role_permission_link import RolePermissionLinkBase
from schemas.base import NonEmptyUpdateModel


class RolePermissionLinkRead(RolePermissionLinkBase):
    pass


class RolePermissionLinkCreate(RolePermissionLinkBase):
    pass


class RolePermissionLinkUpdate(NonEmptyUpdateModel):
    role_id: int | None = None
    permission_id: int | None = None
