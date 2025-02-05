# from celery import Celery
# import os

# celery_app = Celery(
#     "tasks",
#     broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
#     backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0"),
# )

# @celery_app.task
# def add_task(dataRequest):
#     return {
#         "data": dataRequest,
#         "message": "Add task"
#     }
from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)

@celery_app.task
def ping():
    return "Ping successful"
