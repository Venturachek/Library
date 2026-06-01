from src.models.book import BooksOrm
from src.models.loan import LoanOrm
from src.models.telegram_link import TelegramLink as TelegramLinkOrm
from src.schemas.telegram_link import TelegramLink
from src.models.user import UserOrm
from src.repositories.Mapper.base import DataMapper
from src.schemas.books import Book
from src.schemas.loan import Loan
from src.schemas.user import User


class BooksDataMapper(DataMapper):
    model = BooksOrm
    schema = Book

class UserDataMapper(DataMapper):
    model = UserOrm
    schema = User

class LoanDataMapper(DataMapper):
    model = LoanOrm
    schema = Loan

class TelegramLinkDataMapper(DataMapper):
    model = TelegramLinkOrm
    schema = TelegramLink

