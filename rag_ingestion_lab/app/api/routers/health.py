
import logging

from fastapi import APIRouter, HTTPException
from redis.exceptions import RedisError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import engine
from app.core.redis_client import redis_client


router = APIRouter(tags=["Health"])
logger = logging.getLogger(__name__)


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/health/ready")
def readiness():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        if not redis_client.ping():
            raise RedisError("Redis PING failed")

    except (SQLAlchemyError, RedisError, OSError):
        logger.exception("Health check failed")
        raise HTTPException(
            status_code=503,
            detail="Database or Redis unavailable",
        )

    return {
        "status": "ready",
        "postgres": "ok",
        "redis": "ok",
    }
