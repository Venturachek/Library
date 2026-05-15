from sqlalchemy import select
from src.models.loan import LoanOrm
from src.models.user import UserOrm
from src.task.celery_app import celery_instance
from datetime import timedelta, date
from src.services.email import EmailService
from src.database import sync_session_maker

email_service = EmailService()

@celery_instance.task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=3,
)
def send_reminder():
    tomorrow = date.today() + timedelta(days=1)
    with sync_session_maker() as session:
        query = session.execute(
            select(UserOrm.email)
            .join(LoanOrm, LoanOrm.user_id==UserOrm.id)
            .filter(LoanOrm.loan_to==tomorrow,
                    LoanOrm.returned==False)
        )
        emails = query.scalars().all()
        for email in emails:
            email_service.send_email(to_email=email, subject="Reminder", message="Please return book tomorrow")


