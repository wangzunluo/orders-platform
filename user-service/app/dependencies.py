from sqlalchemy.orm import sessionmaker
from .db import get_engine

def get_db():
    engine = get_engine()
    SessionLocal = sessionmaker(bind=engine)

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()