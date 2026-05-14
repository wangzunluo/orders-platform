from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
import os

Base = declarative_base()

def get_engine():
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
            f"{os.getenv('DB_OPTIONS')}"
        )
    print(url)
    return create_engine(url)
