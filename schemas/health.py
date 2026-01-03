from pydantic import BaseModel


class HealthyResponse(BaseModel):
    status: str = "ok"


class UnhealthyResponse(BaseModel):
    status: str = "unhealthy"
