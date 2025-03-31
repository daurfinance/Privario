# backend/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base

DATABASE_URL = "sqlite:///../database/privaro.sqlite"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создать таблицы при запуске
def init_db():
    Base.metadata.create_all(bind=engine)
