from sqlalchemy import Column, Integer, String
from .db import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    item = Column(String)
    status = Column(String, default="created")