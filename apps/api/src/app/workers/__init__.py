from celery import Celery

from app.config import settings

celery_app = Celery(
    "documind",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)

from app.workers.ingestion import *  # noqa: E402, F401, F403
