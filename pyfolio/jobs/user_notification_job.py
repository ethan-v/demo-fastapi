from pyfolio.apps.log.log_func import write_log
from pyfolio.celery import celery


@celery.task(name="notify_user_subscribed_job")
def notify_user_subscribed_job(email: str):
    write_log(message=f"[BACKGROUND JOB][{email}] Sent notification for subscribed user")
    return True

