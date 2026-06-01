from src.repositories.LoanRepository import LoanRepository
from src.repositories.TelegramRepository import TelegramRepository
from src.repositories.UserRepository import UserRepository
from src.repositories.BooksRepository import BooksRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.books = BooksRepository(self.session)
        self.user = UserRepository(self.session)
        self.loan = LoanRepository(self.session)
        self.tg = TelegramRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()