from sqlmodel import SQLModel

# === Health Schemas ===


class HealthyRead(SQLModel):
    status: str = "ok"


class UnhealthyRead(SQLModel):
    status: str = "unhealthy"
