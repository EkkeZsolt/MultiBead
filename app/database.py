from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

class Base(DeclarativeBase):
    pass

engine = create_engine("sqlite:///data.db", echo=False)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal(bind=engine)
    try:
        yield db
    finally:
        db.close()