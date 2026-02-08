from core.repositories.repository import Repository

from .models import Notification
from .schemas import NotificationCreate, NotificationUpdate

# =============================================================================
# Notification Repository
# =============================================================================


class PermissionRepository(
    Repository[Notification, NotificationCreate, NotificationUpdate]
):
    pass
