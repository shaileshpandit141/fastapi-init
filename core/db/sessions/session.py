from sqlalchemy.orm import sessionmaker
from sqlmodel import Session

from ..engines.engine import engine

session = sessionmaker(
    bind=engine,
    class_=Session,
    autoflush=False,
)
