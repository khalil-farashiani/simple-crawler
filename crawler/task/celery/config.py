from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKER,
    backend=settings.CELERY_BACKEND,
)
