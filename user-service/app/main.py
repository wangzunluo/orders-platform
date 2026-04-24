from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .dependencies import get_db
from .db import Base, engine
from contextlib import asynccontextmanager
import time

RETRIES = 5

@asynccontextmanager
async def lifespan(app: FastAPI):
    for _ in range(RETRIES):
        try:
            engine.connect()
            print("Database connection successful")
            engine.close()
            break
        except Exception as e:
            print(f"Database connection failed: {e}")
            time.sleep(3)

    Base.metadata.create_all(bind=engine)
    yield
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user