# Python Outbox Microservice

This is a microservice example implementing the Outbox Pattern for handling order and inventory events.

## Technology Stack

- Python 3.12+
- FastAPI: Web API framework
- SQLAlchemy: ORM
- PostgreSQL: Database
- RabbitMQ: Message queue
- Docker: Containerization

## Features

- Data consistency using the Outbox Pattern
- Asynchronous event processing
- Automatic retry mechanism

## Project Structure

```
python-outbox-microservice/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── models.py        # Database models
│   ├── database.py      # Database connection setup
│   └── worker.py        # Event processing worker
├── dockerfiles/
│   └── python           # Python service Dockerfile
├── docker-compose.yml   # Docker Compose configuration
├── init.sql            # Database initialization script
└── README.md
```

## Event Processing Flow

1. When an API request is received, events are written to the `outbox_messages` table in PostgreSQL
2. The Worker service periodically checks for unprocessed events
3. When unprocessed events are found, the worker:
   - Sends the event to RabbitMQ
   - Updates the event's processing status
4. If sending fails, it will be retried during the next check