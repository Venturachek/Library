from src.repositories.BooksRepository import BooksRepository
from src.repositories.LoanRepository import LoanRepository
from src.repositories.UserRepository import UserRepository


class SyncDBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()


        self.books = BooksRepository(self.session)
        self.user = UserRepository(self.session)
        self.loan = LoanRepository(self.session)

        return self

    def __exit__(self, *args):
        self.session.rollback()
        self.session.close()

    def sync_commit(self):
        self.session.commit()