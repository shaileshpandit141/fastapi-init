from core.repositories.repository import Repository

from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate

# === User Repository ===


class UserRepository(Repository[User, UserCreate, UserUpdate]):
    pass
