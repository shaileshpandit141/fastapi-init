from core.repositories.repository import Repository

from ..models.user_role import UserRole
from ..schemas.user_role import UserRoleCreate, UserRoleUpdate

# === User Role Repository ===


class UserRoleRepository(Repository[UserRole, UserRoleCreate, UserRoleUpdate]):
    pass
