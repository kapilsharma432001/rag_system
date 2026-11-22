from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "rag_ingestion",
    broker=settings.redis_url,
    backend=settings.celery_result_backend,
    include=["app.workers.tasks.health"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_track_started=True,
    result_expires=3600,
)