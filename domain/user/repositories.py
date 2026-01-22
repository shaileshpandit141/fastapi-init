from core.repositories.repository import Repository

from .models import User, UserRole
from .schemas import UserCreate, UserRoleCreate, UserRoleUpdate, UserUpdate

# === User Repository ===


class UserRepository(Repository[User, UserCreate, UserUpdate]):
    pass


# === User Role Repository ===


class UserRoleRepository(Repository[UserRole, UserRoleCreate, UserRoleUpdate]):
    pass
