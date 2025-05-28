import pika
from datetime import datetime, timezone
import json
import time
import logging
from sqlalchemy import select
from .database import SessionLocal, init_db
from .models import OutboxMessage

# 設置日誌格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def process_outbox():
    # 初始化資料庫
    logging.info('初始化資料庫...')
    init_db()
    
    # RabbitMQ 訊息發送改為每次都建立新連線與 channel
    while True:
        with SessionLocal() as session:
            stmt = select(OutboxMessage).where(OutboxMessage.processed_at.is_(None)).limit(10)
            events = session.scalars(stmt).all()
            if events:
                logging.info(f'找到 {len(events)} 個未處理的事件')

            for event in events:
                try:
                    logging.info(f'處理事件 {event.id} (類型: {event.event_type})')
                    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
                    channel = connection.channel()
                    channel.queue_declare(queue='order_events')
                    channel.basic_publish(
                        exchange='',
                        routing_key='order_events',
                        body=json.dumps(event.payload)
                    )
                    channel.close()
                    connection.close()
                    event.processed_at = datetime.now(timezone.utc)
                    session.commit()
                    logging.info(f'事件 {event.id} 處理成功並發送到 RabbitMQ')
                except Exception as e:
                    logging.error(f'處理事件 {event.id} 時發生錯誤: {str(e)}')
                    session.rollback()

        time.sleep(5)  # 每 5 秒查詢一次

if __name__ == "__main__":
    process_outbox()
