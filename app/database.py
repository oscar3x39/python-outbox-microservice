from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from .models import Base
import logging

logging.basicConfig(level=logging.INFO)

DATABASE_URL = "postgresql://user:pass@db:5432/mydb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    inspector = inspect(engine)
    logging.info(f'現有資料表: {inspector.get_table_names()}')
    logging.info('開始創建資料表...')
    Base.metadata.create_all(bind=engine)
    logging.info(f'資料表創建完成，現有資料表: {inspect(engine).get_table_names()}')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
