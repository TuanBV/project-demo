from celery import Celery
import os
import redis

celery_app = Celery(
    "tasks",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0"),
)

redis_client = redis.Redis.from_url(os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"))

@celery_app.task
def check_queue():
    queue_length = redis_client.llen("celery")
    print(f"Queue length: {queue_length}")
    if queue_length > 0:
        print("Tasks are waiting in the queue!")
    else:
        print("Queue is empty!")
