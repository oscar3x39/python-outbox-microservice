from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime
from .database import get_db
from .models import OutboxMessage
from pydantic import BaseModel

app = FastAPI(title="Outbox Microservice")

class OrderCreate(BaseModel):
    product_id: str
    quantity: int
    customer_id: Optional[str] = None

from uuid import UUID

class OutboxMessageResponse(BaseModel):
    id: UUID
    event_type: str
    payload: dict
    created_at: datetime
    processed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

@app.post("/orders", response_model=OutboxMessageResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """建立訂單並產生 OrderCreated 事件"""
    event = OutboxMessage(
        event_type="OrderCreated",
        payload={
            "product_id": order.product_id,
            "quantity": order.quantity,
            "customer_id": order.customer_id,
            "order_date": datetime.utcnow().isoformat()
        }
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

@app.post("/inventory/adjust", response_model=OutboxMessageResponse)
def adjust_inventory(product_id: str, quantity: int, db: Session = Depends(get_db)):
    """調整庫存並產生 InventoryAdjusted 事件"""
    event = OutboxMessage(
        event_type="InventoryAdjusted",
        payload={
            "product_id": product_id,
            "quantity_change": quantity,
            "adjustment_date": datetime.utcnow().isoformat()
        }
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

@app.get("/events", response_model=List[OutboxMessageResponse])
def list_events(
    processed: Optional[bool] = None,
    event_type: Optional[str] = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """列出所有事件，可以按處理狀態和事件類型篩選"""
    query = select(OutboxMessage)
    
    if processed is not None:
        if processed:
            query = query.where(OutboxMessage.processed_at.is_not(None))
        else:
            query = query.where(OutboxMessage.processed_at.is_(None))
    
    if event_type:
        query = query.where(OutboxMessage.event_type == event_type)
    
    query = query.limit(limit)
    events = db.scalars(query).all()
    return events

@app.get("/events/{event_id}", response_model=OutboxMessageResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    """取得單一事件的詳細資訊"""
    event = db.get(OutboxMessage, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event