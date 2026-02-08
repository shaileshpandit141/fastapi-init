from core.repositories.repository import Repository

from .models import Notification
from .schemas import NotificationCreate, NotificationUpdate

# =============================================================================
# Notification Repository
# =============================================================================


class NotificationRepository(
    Repository[Notification, NotificationCreate, NotificationUpdate]
):
    pass
