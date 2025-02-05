from celery import Celery
from celery.schedules import crontab
from tasks import check_queue
import os


celery_app = Celery(
    "worker",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0"),
    include=["tasks"],
)

celery_app.conf.beat_schedule = {
    "check-queue-every-5-minutes": {
        "task": "tasks.check_queue",
        "schedule": crontab(minute="*/1"),  # Mỗi 5 phút
    },
}
celery_app.conf.timezone = "UTC"
