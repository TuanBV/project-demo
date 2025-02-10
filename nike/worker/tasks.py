from celery.result import AsyncResult
from celery import Celery
import os
import redis

celery_app = Celery(
    "tasks",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0"),
    include=["tasks"],
)

redis_client = redis.Redis.from_url(os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"))

@celery_app.task
def check_queue():
    """
    Celery task to check the queue length and print a message.
    """
    print("------------------------")
    queue_length = redis_client.llen("celery")
    print(f"Queue length: {queue_length}")
    if queue_length > 0:
        print("Tasks are waiting in the queue!")
    else:
        print("Queue is empty!")

@celery_app.task
def add_task(dataRequest):
    return { "data": dataRequest }


def get_task_result(task_id):
    result = AsyncResult(task_id, app=celery_app)
    if result.successful():
        # Chỉnh sửa message trong kết quả trả về
        data = result.result
        if isinstance(data, dict) and "message" in data:
            data["message"] = "Task completed successfully"  # Thay đổi giá trị message
        return data  # Trả về kết quả đã sửa
    return {"status": "PENDING", "message": "Task is still running"}


def retry_send_mail(id_user, max_retries=3):
    """
    This function send an mail using the ID and can retry 3 times.
    Parameters:
    id (str): Id of user.
    max_retries (int, optional): The maximum number of times to retry sending the email is 3.

    Returns: Status send mail
    """
    time_retry = 0
    while time_retry < max_retries:
        time_retry += 1
        try:
            return retry_send_mail(id_user)
        except Exception as e:
            print(f"Retrying ...{e}")

    return "Fail"


def send_mail(id):
    return "Success"
