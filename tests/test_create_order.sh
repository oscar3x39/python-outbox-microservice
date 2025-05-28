#!/bin/bash
# 建立訂單測試
curl -X POST http://localhost:8000/orders \
  -H 'Content-Type: application/json' \
  -d '{
    "product_id": "PROD-001",
    "quantity": 3,
    "customer_id": "CUST-001"
  }'
