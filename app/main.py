from fastapi import FastAPI

from app.shared.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app.APP_NAME,
    debug=settings.app.DEBUG,
)
