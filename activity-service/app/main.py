from fastapi import FastAPI
from pymongo import MongoClient
from datetime import datetime, timezone
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017/")

client = MongoClient(MONGO_URL)
db = client["activity_db"]
collection = db["events"]

app = FastAPI()

@app.post("/event")
def create_event(event: dict):
    event["timestamp"] = datetime.now(timezone.utc)
    collection.insert_one(event)
    return {"status": "Event created successfully"}

@app.get("/events")
def get_events():
    events = list(collection.find({}, {"_id": 0}))
    return {"events": events}