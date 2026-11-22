import logging

from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from redis.exceptions import RedisError
from sqlalchemy.exc import SQLAlchemyError

from app.db import engine
from app.redis_client import redis_client

from pydantic import BaseModel
from app.celery_app import celery_app
from app.tasks import simulate_ingestion


logger = logging.getLogger(__name__)

app = FastAPI(title="RAG Ingestion API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/health/ready")
def readiness():
    try:
        # check postgreSQL
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        # check redis
        if not redis_client.ping():
            raise RedisError("Redis PING failed")

    except (SQLAlchemyError, RedisError, OSError):
        logger.exception("Dependency health check failed")
        raise HTTPException(
            status_code=503,
            detail = "Database or Redis unavailable"
        )

    return {
        "status": "ready",
        "postgres": "ok",
        "redis": "ok"
    }


class DemoIngestionRequest(BaseModel):
    filename: str

@app.post("/demo/ingestion", status_code=202)
def start_ingestion(request: DemoIngestionRequest):
    task = simulate_ingestion.delay(request.filename)

    return {
        "task_id": task.id,
        "status": "submitted",
    }

@app.get("/demo/ingestion/{task_id}")
def get_ingestion_status(task_id: str):
    task = celery_app.AsyncResult(task_id)

    response = {
        "task_id": task_id,
        "status": task.state
    }

    if task.successful():
        response["result"] = task.result

    elif task.failed():
        response["error"] = "Task processing failed"


    return response