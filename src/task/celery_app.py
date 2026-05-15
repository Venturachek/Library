from celery import Celery

from src.config import settings

celery_instance = Celery("task", broker=settings.redis_url, include=["src.task.tasks"])

celery_instance.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Berlin",
)
