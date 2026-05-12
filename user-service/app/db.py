from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

def build_database_url():
    if os.getenv("DATABASE_URL"):
        print("using DATABASE_URL")
        return os.getenv("DATABASE_URL")

    print("building DATABASE_URL from parts")
    return (
        f"postgresql://{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:"
        f"{os.getenv('DB_PORT')}/"
        f"{os.getenv('DB_NAME')}"
    )
DATABASE_URL = build_database_url()
print(DATABASE_URL.split('@')[-1])
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
