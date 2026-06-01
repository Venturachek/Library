from datetime import timedelta, date
import secrets
import string
from src.utils.sync_dbmanager import SyncDBManager
from src.database import sync_session_maker
from sqlalchemy import select

from src.models.book import BooksOrm
from src.models.loan import LoanOrm
from src.models.user import UserOrm


def get_emails():
    tomorrow = date.today() + timedelta(days=1)
    with SyncDBManager(session_factory=sync_session_maker) as db:
        query = db.session.execute(
            select(UserOrm.email, BooksOrm.title)
            .join(LoanOrm, LoanOrm.user_id == UserOrm.id)
            .join(BooksOrm, BooksOrm.id == LoanOrm.book_id)
            .filter(LoanOrm.loan_to == tomorrow,
                LoanOrm.returned == False))
        res = [
    {"email": email, "title": title}
    for email, title in query.all()
    ]
        print(res)
        return res

def generate_code(length: int = 6) -> str:
    alphabet = string.ascii_uppercase + string.digits
    return "".join([secrets.choice(alphabet) for i in range(length)])
