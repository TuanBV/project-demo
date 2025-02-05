from celery import Celery
import os

celery_app = Celery(
    "task",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0"),
)

@celery_app.task
def add_task(x, y):
    return x + y
