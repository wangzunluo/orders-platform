from fastapi import FastAPI, Request
from pymongo import MongoClient
from datetime import datetime, timezone
import os
import asyncio
from contextlib import asynccontextmanager

RETRIES = 5

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

@asynccontextmanager
async def lifespan(app: FastAPI):
    for i in range(RETRIES):
        try:
            print(f"Attempt {i+1}: Connecting to Mongo...")
            client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=3000)
            client.server_info()
            db = client["activity_db"]
            app.state.collection = db["events"]
            app.state.client = client
            print('connected to mongo')
            break
        except Exception as e:
            print(f"mongo connection failed: {e}")
            await asyncio.sleep(3)
    else:
        raise RuntimeError("Could not connect to Mongo after retries")
    yield
    print("Shutting down...")
    app.state.client.close()

app = FastAPI(lifespan=lifespan)

@app.post("/event")
def create_event(event: dict, request: Request):
    event["timestamp"] = datetime.now(timezone.utc)
    request.app.state.collection.insert_one(event)
    return {"status": "Event created successfully"}

@app.get("/events")
def get_events(request: Request):
    events = list(request.app.state.collection.find({}, {"_id": 0}))
    return {"events": events}