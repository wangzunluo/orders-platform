from app.db import Base, get_engine
from app import models  # ensures models are registered

engine = get_engine()
print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done")