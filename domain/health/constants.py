from enum import Enum


class HealthCache(Enum):
    KEY = "health_status"
    HEALTHY_TTL = 30  # seconds
    UNHEALTHY_TTL = 5  # seconds
