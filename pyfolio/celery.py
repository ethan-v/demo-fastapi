import os
import time

from celery import Celery

from pyfolio.apps.log.log_func import write_log

celery = Celery(__name__)
# celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
# celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")
celery.conf.broker_url = "redis://localhost:6379"
celery.conf.result_backend = "redis://localhost:6379"


@celery.task(name="notify_user_subscribed_job")
def notify_user_subscribed_job(email: str):
    write_log(message=f"[BACKGROUND JOB][{email}] Sent notification for subscribed user")
    return True
