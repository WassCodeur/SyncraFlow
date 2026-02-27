from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "SyncraFlow",
    broker=settings.REDIS_DB,
    backend=settings.REDIS_DB,
    include=["app.works.tasks"]
)
