from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON, Uuid
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4

Base = declarative_base()

class OutboxMessage(Base):
    __tablename__ = "outbox_messages"

    id = Column(Uuid, primary_key=True, default=uuid4)
    event_type = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    processed_at = Column(DateTime, nullable=True)
