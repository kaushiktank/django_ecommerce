from celery.decorators import task
from celery.utils.log import get_task_logger

from .email import send_order_email

logger = get_task_logger(__name__)

@task(name="send_order_email_task")
def send_order_email_task(name, email, order, email_file):
    logger.info("Sent order email")
    return send_order_email(name, email, order, email_file)
