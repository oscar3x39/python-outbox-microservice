from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, JSON, String, UUID, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid

SQLALCHEMY_DATABASE_URL = "postgresql://user:pass@db:5432/mydb"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class OutboxMessage(Base):
    __tablename__ = 'outbox_messages'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    event_type = Column(String(50), nullable=False)
    payload = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    processed_at = Column(DateTime, nullable=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
