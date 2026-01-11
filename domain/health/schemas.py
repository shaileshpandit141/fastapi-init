from sqlmodel import SQLModel


class HealthyRead(SQLModel):
    status: str = "ok"


class UnhealthyRead(SQLModel):
    status: str = "unhealthy"
