from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import pathlib
import os

# .env betöltése a projekt gyökérből
env_path = pathlib.Path(__file__).parents[1] / ".env"
load_dotenv(env_path)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data.db")

class Base(DeclarativeBase):
    pass

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal(bind=engine)
    try:
        yield db
    finally:
        db.close()