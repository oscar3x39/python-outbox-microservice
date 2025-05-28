#!/bin/bash
# 調整庫存測試
curl -X POST "http://localhost:8000/inventory/adjust?product_id=PROD-001&quantity=5"
