from fastapi import FastAPI
from pymongo import MongoClient
from datetime import datetime, timezone
import os

def build_database_url():
    if os.getenv("MONGO_URL"):
        print("using MONGO_URL")
        return os.getenv("MONGO_URL")

    print("building DATABASE_URL from parts")
    return (
        f"mongodb://{os.getenv('MONGO_USER')}:"
        f"{os.getenv('MONGO_PASSWORD')}@"
        f"{os.getenv('MONGO_HOST')}:"
        f"{os.getenv('MONGO_PORT')}/"
        f"{os.getenv('MONGO_OPTIONS')}"
    )
MONGO_URL = build_database_url()
print(MONGO_URL.split('@')[-1])
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