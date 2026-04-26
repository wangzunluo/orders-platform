from fastapi import FastAPI, HTTPException, Depends
import requests
from .db import Base, engine
from . import models
from sqlalchemy.orm import Session
from .dependencies import get_db
import time
from contextlib import asynccontextmanager

RETRIES = 5
USER_SERVICE_URL = "http://user-service"
ACTIVITY_SERVICE_URL = "http://activity-service:80/event"

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

@app.post("/orders")
def create_order(user_id: int, item: str, db: Session = Depends(get_db)):
    r = requests.get(f"{USER_SERVICE_URL}/users/{user_id}")
    if r.status_code == 400:
        raise HTTPException(status_code=400, detail="Invalid user_id")
    if r.status_code != 200:
        raise HTTPException(status_code=500, detail="User service error")
    order = models.Order(user_id=user_id, item=item, status="created")
    db.add(order)
    db.commit()
    db.refresh(order)
    event = {
        "user_id": user_id,
        "service": "order-service",
        "event_type": "order_created",
        "details": {
            "order_id": order.id,
            "item": item
        }
    }
    requests.post(ACTIVITY_SERVICE_URL, json=event)
    return order

@app.get("/orders/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order