from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas
from .dependencies import get_db
from .db import Base, get_engine
from contextlib import asynccontextmanager
import asyncio

RETRIES = 5

@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = get_engine()
    for _ in range(RETRIES):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Database connection successful")
            break
        except Exception as e:
            print(f"Database connection failed: {e}")
            await asyncio.sleep(3)
    else:
        raise RuntimeError("Could not connect to DB after retries")
    yield
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user