from fastapi import FastAPI
from pymongo import MongoClient
from datetime import datetime, timezone
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017/")

if "MONGO_USER" in os.environ:
    MONGO_URL = (
        f"mongodb://{os.getenv('MONGO_USER')}:"
        f"{os.getenv('MONGO_PASSWORD')}@"
        f"{os.getenv('MONGO_HOST')}:"
        f"{os.getenv('MONGO_PORT')}/"
        f"{os.getenv('MONGO_OPTIONS')}"
    )
else:
    print('creating mongo url from default local mongodb')
    MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017/")
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