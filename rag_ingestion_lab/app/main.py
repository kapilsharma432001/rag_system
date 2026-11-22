import logging

from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from redis.exceptions import RedisError
from sqlalchemy.exc import SQLAlchemyError

from app.db import engine
from app.redis_client import redis_client


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
