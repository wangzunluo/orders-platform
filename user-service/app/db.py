from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

Base = declarative_base()
engine = None
SessionLocal = None

def get_engine():
    global engine, SessionLocal
    if engine:
        return engine
    
    if os.getenv("DATABASE_URL"):
        print("using DATABASE_URL")
        url = os.getenv("DATABASE_URL")
    else:
        print("building DATABASE_URL from parts")
        url = (
            f"postgresql://{os.getenv('DB_USER')}:"
            f"{os.getenv('DB_PASSWORD')}@"
            f"{os.getenv('DB_HOST')}:"
            f"{os.getenv('DB_PORT')}/"
            f"{os.getenv('DB_NAME')}"
        )
        
    print(url.split('@')[-1])
    engine = create_engine(url)
    SessionLocal = sessionmaker(bind=engine)
    return engine
