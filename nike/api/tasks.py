from celery import Celery
import os

celery_app = Celery(
    "tasks",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0"),
)

def add_task(dataRequest):
    return celery_app.send_task("tasks.add_task", args=[dataRequest])
