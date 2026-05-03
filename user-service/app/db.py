from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

if "DB_USER" in os.environ:
    print('creating db url from ECS config')
    DATABASE_URL = (
        f"postgresql://{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:"
        f"{os.getenv('DB_PORT')}/"
        f"{os.getenv('DB_NAME')}"
    )
else:
    print('creating db url from EC2 env file')
    DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
