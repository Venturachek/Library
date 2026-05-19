from src.task.celery_app import celery_instance
from src.repositories.utils import get_emails
from src.services.email import EmailService
import logging

email_service = EmailService()

@celery_instance.task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=3,
)
def send_reminder():
    logging.info("Sending reminder")

    emails = get_emails()
    logging.info(f"Found {len(emails)} emails")

    for item in emails:
        email = item["email"]
        title = item["title"]

        email_service.send_email(
            to_email=email,
            subject="Reminder",
            message=f"Please return {title} tomorrow"
        )


