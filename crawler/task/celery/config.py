from celery import Celery
from app.core.config import settings


def make_celery(app_name=__name__):
    celery_app =  Celery(
        app_name,
        broker=settings.CELERY_BROKER,
        backend=settings.CELERY_BACKEND,
    )
    return celery_app


celery_app = make_celery("worker")
