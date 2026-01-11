from core.db.base import NonEmptyUpdateModel
from domain.rbac.models import RolePermissionLinkBase


class RolePermissionLinkRead(RolePermissionLinkBase):
    pass


class RolePermissionLinkCreate(RolePermissionLinkBase):
    pass


class RolePermissionLinkUpdate(NonEmptyUpdateModel):
    role_id: int | None = None
    permission_id: int | None = None
