from enum import StrEnum

# =============================================================================
# Notification Category
# =============================================================================


class NotificationCategory(StrEnum):
    SYSTEM = "system"
    SOCIAL = "social"
    WORKFLOW = "workflow"
    COMMERCE = "commerce"


# =============================================================================
# Notification Event
# =============================================================================


class NotificationEvent(StrEnum):
    SYSTEM = "system"
    SECURITY = "security"
    BILLING = "billing"
    COMMENT = "comment"
    LIKE = "like"
    MENTION = "mention"

    @property
    def category(self) -> NotificationCategory:
        if self in {
            NotificationEvent.SYSTEM,
            NotificationEvent.SECURITY,
            NotificationEvent.BILLING,
        }:
            return NotificationCategory.SYSTEM

        return NotificationCategory.SOCIAL


# =============================================================================
# Event MAP SET HELPERS
# =============================================================================


SYSTEM_EVENTS = {
    NotificationEvent.SYSTEM,
    NotificationEvent.SECURITY,
    NotificationEvent.BILLING,
}

SOCIAL_EVENTS = {
    NotificationEvent.COMMENT,
    NotificationEvent.LIKE,
    NotificationEvent.MENTION,
}
