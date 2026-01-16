from core.repository.base import AsyncRepository

from ..models.user_role import UserRole
from ..schemas.user_role import UserRoleCreate, UserRoleUpdate

# === User Role Repository ===


class UserRoleRepository(AsyncRepository[UserRole, UserRoleCreate, UserRoleUpdate]):
    pass
